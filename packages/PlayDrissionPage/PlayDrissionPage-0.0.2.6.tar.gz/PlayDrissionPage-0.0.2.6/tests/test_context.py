from dotenv import load_dotenv
load_dotenv()
if __name__ == '__main__':
    from PlayDrissionPage.client.remote_browser_client import RemoteBrowserClient

    rbc = RemoteBrowserClient()
    page = rbc.get_d_page(user_id='Default')

