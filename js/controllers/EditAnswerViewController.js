import PostButtonViewController from '~/controllers/PostButtonViewController';
import ActionControllerDelegate from '~/delegate/ActionControllerDelegate';
import SwappingViewController from '~/controllers/SwappingViewController';
import Analytics, { EventType } from '~/models/Analytics';
import PublishEdit from '~/models/Request/PublishEdit';
import ErrorManager from '~/helpers/ErrorManager';

export default class EditAnswerViewController extends PostButtonViewController {
    static activeEditInstance = null;

    /**
     * @param {Object} o options
     * @param {HTMLElement} o.trigger Trigger for deletion
     * @param {AnswerViewController} o.answerController the controller for the answer
     */
    constructor({ trigger, answerController }) {
        super(trigger);

        /** @type {AnswerViewController} */
        this.answerController = answerController;

        /** @private */
        this.editor = new SwappingViewController(this.answerController.body);

        trigger.addEventListener("click", ::this.trigger);

        /** @type {boolean} */
        this.isEditing = false;
    }

    /**
     * Open editor
     */
    async trigger() {
        if (this.isEditing) return;
        this.isEditing = true;

        EditAnswerViewController.activeEditInstance?.untrigger(false);
        EditAnswerViewController.activeEditInstance = this;

        Analytics.shared.report(EventType.answerEditClick(this.answerController.answer));

        this.isLoading = true;

        // Load the template
        const { default: AnswerEditTemplate } = await import('~/template/AnswerEditTemplate');
        const answerEditor = await new AnswerEditTemplate(this.answerController.answer);
        this.editor.displayAlternate(answerEditor);

        const originalByteCount = this.answerController.byteCount;
        const answerEncoding = this.answerController.answer.language.encoding();

        answerEditor.navigationDelegate.shouldClose = async (controller, context) => {
            if (context) {
                await this.edit(context);
                this.untrigger(true);
            } else {
                this.answerController.byteCount = originalByteCount;
                this.untrigger(false);
            }
        };

        answerEditor.actionDelegate.didSetStateTo = (controller, code) => {
            this.answerController.byteCount = answerEncoding.byteCount(code);
        };

        this.isLoading = false;
        this.isDisabled = true;
    }

    /**
     * Submits edits
     * @param {Answer} newAnswer - The new answer object (should be same ID).
     * @return {Answer} The new answer object
     */
    async edit(newAnswer) {
        const publishEdit = new PublishEdit({
            item: newAnswer,
            original: this.answerController.answer
        });

        const finalAnswer = await publishEdit.run();
        await this.answerController.setAnswer(finalAnswer);
        return finalAnswer;
    }

    /**
     * Close editor
     * @param {boolean} changesUpdated - If the changes should be displayed
     */
    untrigger(changesUpdated = false) {
        if (!this.isEditing) return;
        this.isEditing = false;

        this.isDisabled = false;
        this.editor.restoreOriginal();

        if (changesUpdated) {
            Analytics.shared.report(EventType.answerEdited(this.answerController.answer));
        } else {
            Analytics.shared.report(EventType.answerNotEdited(this.answerController.answer));
        }
        EditAnswerViewController.activeEditInstance = null;
    }
}
