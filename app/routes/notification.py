from app.controllers import notifications
from app.models.Answer import Answer
from app.models.User import User
from app.session.csrf import csrf_protected
from app.helpers.render import render_json, render_enum
from app.server import server

from flask import abort, redirect, url_for, g


@server.route('/notifications/status')
@csrf_protected
def notification_status():
    if not isinstance(g.user, User):
        return render_error('Unauthorized'), 401

    unseen_notifs = notifications.get_unseen_notification_count()

    if not isinstance(unseen_notifs, int):
        return unseen_notifs

    return render_json({
        'unseen_count': unseen_notifs
    })

@server.route('/notification/enum/statuses')
def get_notification_enum_statuses():
    return render_enum(notifications.get_notification_statuses())

@server.route('/notification/enum/types')
def get_notification_enum_types():
    return render_enum(notifications.get_notification_types())

@server.route('/notifications/all/page/<int:page>', methods=['GET'])
@csrf_protected
def get_notification_page(page):
    if not isinstance(g.user, User):
        return render_error('Unauthorized'), 401

    return notifications.get_notification_page(page)

@server.route('/responder/<notification_id>/<name>/<target_id>')
def notification_responder(notification_id, name, target_id):
    # If it exists we'll mark the notification as read. If the
    # user is unauthorized then OK we don't really care too
    # much so we'll ignore the 404 in the case
    notifications.mark_notification_read(notification_id)

    responder_parameter = f'n.{notification_id}'

    try:
        parsed_id = int(target_id)
    except ValueError:
        parsed_id = None

    if name == 'answer':
        if parsed_id is None:
            return abort(404)

        answer = Answer.query.filter_by(id=parsed_id).first()
        if answer is None:
            return abort(404)

        return redirect(url_for('get_post', post_id=answer.post_id, s=responder_parameter), code=301)

    if name == 'post':
        if parsed_id is None:
            return abort(404)

        return redirect(url_for('get_post', post_id=parsed_id, s=responder_parameter), code=301)

    return abort(404)
