import WebC__API_Markdown_To_Html   from "../../../js/elements/api/WebC__API_Markdown_To_Html.mjs";
import Web_Component                from "../../../js/core/Web_Component.mjs";
import API__Invoke                  from "../../../js/data/API__Invoke.mjs";
import WebC__Target_Div             from "../../../js/utils/WebC__Target_Div.mjs";

QUnit.module('WebC__API_Markdown_To_Html', function(hooks) {
    let target_div
    let webc__api_markdown_to_html
    let mock_responses
    let api_path
    let content_path

    hooks.beforeEach(async (assert) =>{
        content_path               = 'en/web-pages/demos/index.md'
        target_div                 = WebC__Target_Div.add_to_body()
        mock_responses             = JSON.stringify(api_mock_data())
        let attributes             = { content_path:content_path, mock_responses: mock_responses, api_path: api_path }
        webc__api_markdown_to_html = await target_div.append_child(WebC__API_Markdown_To_Html, attributes)
    })

    function api_mock_data() {
        const url__api_markdown_content  = WebC__API_Markdown_To_Html.url__api_markdown_content + content_path
        const url__api_markdown_to_html  = WebC__API_Markdown_To_Html.url__api_markdown_to_html
        return { [url__api_markdown_content]: expected_markdown ,
                 [url__api_markdown_to_html]: expected_raw_html }
    }
    hooks.afterEach(() => {
        webc__api_markdown_to_html.remove()
        target_div                .remove()
    })

    QUnit.test('.constructor', (assert) => {
        assert.deepEqual(target_div.constructor.name                         , 'WebC__Target_Div'                            )
        assert.deepEqual(WebC__API_Markdown_To_Html.name                     , 'WebC__API_Markdown_To_Html'                  )
        assert.deepEqual(webc__api_markdown_to_html.content_path             , content_path                                  )
        assert.deepEqual(webc__api_markdown_to_html.getAttributeNames()      , ['content_path', 'mock_responses', 'api_path'])
        assert.deepEqual(webc__api_markdown_to_html.api_invoke.mock_responses, JSON.parse(mock_responses)                    )

        assert.ok       (WebC__API_Markdown_To_Html.prototype      instanceof Web_Component     )
        assert.ok       (webc__api_markdown_to_html                instanceof Web_Component     )
        assert.ok       (webc__api_markdown_to_html                instanceof HTMLElement       )
        assert.ok       (webc__api_markdown_to_html.api_invoke     instanceof API__Invoke       )
    })

    QUnit.test('.build', (assert) => {
        assert.deepEqual(webc__api_markdown_to_html.markdown_content       , expected_markdown)
        assert.deepEqual(webc__api_markdown_to_html.markdown_html          , expected_raw_html    )
        assert.deepEqual(webc__api_markdown_to_html.shadow_root().innerHTML, expected_html    )
    })

    QUnit.test('static.on_error_return_value', async (assert) => {
        assert.deepEqual(webc__api_markdown_to_html.content_path, content_path)
        await webc__api_markdown_to_html.load_markdown_content()
        assert.deepEqual(webc__api_markdown_to_html.markdown_content, expected_markdown)

        webc__api_markdown_to_html.content_path = 'aaaa/bbbb/cccc.md'
        await webc__api_markdown_to_html.load_markdown_content()
        assert.deepEqual(webc__api_markdown_to_html.markdown_content, WebC__API_Markdown_To_Html.on_error_return_value)
    })

    const expected_raw_html = `<h1>Markdown content</h1><ul><li>will go here</li></ul>`
    const expected_html     = `<div class="${WebC__API_Markdown_To_Html.class_markdown_content}">${expected_raw_html}</div>\n`
    const expected_markdown = "#Markdown content\n\n- will go here"
})

