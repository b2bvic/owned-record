def test_nested_boilerplate_can_be_removed(tool):
    soup = tool.clean_html('<body><div class="cookie"><span>Remove</span></div><main><h1>Keep</h1><p>Body text</p></main></body>')
    assert "Remove" not in soup.get_text()
    assert "Keep" in soup.get_text()


def test_conversion_keeps_links_and_headings(tool):
    soup = tool.clean_html('<body><h1>Title</h1><p><a href="https://example.com">Link</a></p></body>')
    markdown = tool.html_to_markdown(soup)
    assert "# Title" in markdown
    assert "[Link](https://example.com)" in markdown


def test_cli_help(tool):
    from click.testing import CliRunner
    result = CliRunner().invoke(tool.main, ["--help"])
    assert result.exit_code == 0, result.output
    assert "Usage:" in result.output
