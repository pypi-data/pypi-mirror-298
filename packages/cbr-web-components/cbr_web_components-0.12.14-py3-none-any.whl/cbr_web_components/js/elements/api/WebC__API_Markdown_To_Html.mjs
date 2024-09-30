import Web_Component from "../../core/Web_Component.mjs";
import API__Invoke   from "../../data/API__Invoke.mjs";
import Div           from "../../core/Div.mjs";

export default class WebC__API_Markdown_To_Html extends Web_Component {

    static url__api_markdown_content = '/markdown/static_content/content-file?path='
    static url__api_markdown_to_html = '/markdown/render/markdown-to-html'
    static class_markdown_content    = 'markdown_content'
    static on_error_return_value     = `(error loading markdown content)`

    constructor() {
        super();
    }

    // base class methods overrides
    async connectedCallback() {
        super.connectedCallback()
        await this.setup()
        await this.build()
        this.raise_event('build-complete')

    }

    load_attributes() {
        super.load_attributes()
        this.content_path  = this.getAttribute('content_path') || WebC__API_Markdown_To_Html.path__test_page
    }

    // class methods

    async build() {
        const div_class = WebC__API_Markdown_To_Html.class_markdown_content
        const div_html = new Div({class:div_class , value:this.markdown_html})
        const html     = div_html.html()
        this.set_inner_html(html)
        this.add_css_rules(this.css_rules())
    }

    css_rules() {
        const div_class = WebC__API_Markdown_To_Html.class_markdown_content
        return { [`.${div_class}`] : { 'background-color': '#F0F0FF' ,
                                       'margin'         : '10px'     ,
                                       'padding'        : '10px'     }}

    }

    async load_html_content() {
        const method           = 'POST'
        const data             = {'text': this.markdown_content}
        const target_url       = WebC__API_Markdown_To_Html.url__api_markdown_to_html
        this.markdown_html     = await this.api_invoke.invoke_api(target_url, method, data)
    }

    async load_markdown_content() {
        this.api_invoke.on_error_return_value = WebC__API_Markdown_To_Html.on_error_return_value
        const method           = 'GET'
        const target_url       = WebC__API_Markdown_To_Html.url__api_markdown_content + this.content_path
        this.markdown_content  = await this.api_invoke.invoke_api(target_url, method)
    }


    async setup() {
        this.markdown_content = null
        this.markdown_html    = null
        this.api_invoke                = new API__Invoke()
        this.api_invoke.mock_responses = JSON.parse(this.getAttribute('mock_responses'))
        await this.load_markdown_content()
        await this.load_html_content()
    }


}

WebC__API_Markdown_To_Html.define()