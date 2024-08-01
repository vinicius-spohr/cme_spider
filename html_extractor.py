from playwright.sync_api import sync_playwright


def html_parser(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    with sync_playwright() as p:
        browser = p.firefox.launch()
        page = browser.new_page(user_agent=user_agent)

        page.route("**/*", lambda route: route.abort() if route.request.resource_type == "image" else route.continue_())
        page.route('**/*', lambda route: route.abort() if route.request.method.lower() == 'post' else route.continue_())

        page.goto(url)

        try:
            load_all_btn = page.locator('button.load-all')
        except Exception as e:
            print(f'Unable to load full page. Error: {e}')
            return None

        load_all_btn.click()
        html = page.content()
        browser.close()

        return html
