import Template from '~/template/Template';

export default class HeaderTemplate extends Template {
    /**
     * A title
     * @param {string} title
     * @param {Object} opts
     * @param {number} [level=1] - The header level
     * @param {?string} opts.subtitle - Optional subtitle. If not provided initially then cannot be set later
     * @param {?ButtonTemplate} opts.button - Button to put in header
     */
    constructor(title, { level = 1, subtitle = null, button = null } = {}) {
        super(<div/>);

        const header = document.createElement(`h${level}`);
        header.appendChild(this.defineLinkedText('title', `${title}`))

        this.underlyingNode.appendChild(
            <DocumentFragment>
                <div class="list-header">
                    { header }
                    { button ? button.unique() : <DocumentFragment/> }
                </div>
                { subtitle ? (
                    <div class="list-header list-header--style-caption">
                        <h2 class="header--style-caption">{ this.defineLinkedText('subtitle', subtitle) }</h2>
                    </div>
                ) : <DocumentFragment/> }
            </DocumentFragment>
        );

        this.defineLinkedClass('isDimmed', 'header--style-dim', header);
    }
}
