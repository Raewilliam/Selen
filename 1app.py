from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
import random

@app.route('/submit', methods=['POST'])
def submit():
    # Get the form data
    email = request.form['email']
    password = request.form['password']
    two_factor = request.form['two_factor']

    # Set up the Chrome driver with headless option and user-agent
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    chrome_options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(options=chrome_options)

    # Set up the rotating IP/proxy
    # proxy_list = ['http://proxy1.com', 'http://proxy2.com', 'http://proxy3.com']
    # proxy = Proxy()
    # proxy.proxy_type = ProxyType.MANUAL
    # proxy.http_proxy = random.choice(proxy_list)
    # proxy.ssl_proxy = random.choice(proxy_list)
    # capabilities = webdriver.DesiredCapabilities.CHROME
    # proxy.add_to_capabilities(capabilities)

    # Navigate to the DoorDash login page with the rotating IP/proxy
    driver.get('https://www.doordash.com/consumer/login/', desired_capabilities=capabilities)

    # Fill in the login form
    email_input = driver.find_element_by_name('email')
    email_input.send_keys(email)

    password_input = driver.find_element_by_name('password')
    password_input.send_keys(password)

    login_button = driver.find_element_by_xpath("//button[@type='submit']")
    login_button.click()

    # Check if two-factor authentication is required
    try:
        two_factor_input = driver.find_element_by_name('twoFactorCode')
        two_factor_input.send_keys(two_factor)

        two_factor_button = driver.find_element_by_xpath("//button[@type='submit']")
        two_factor_button.click()
    except:
        pass

    # Generate the unique link
    orders_link = 'https://www.doordash.com/orders/?token=' + email + password

    # Send the link to the user's email
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', email, 'Subject: Your DoorDash Orders Link\n\n' + orders_link)
    server.quit()

    # Close the Chrome driver
    driver.quit()

    # Get the json object and check if it's valid with the rotating IP/proxy
    proxy.http_proxy = random.choice(proxy_list)
    proxy.ssl_proxy = random.choice(proxy_list)
    capabilities = webdriver.DesiredCapabilities.CHROME
    proxy.add_to_capabilities(capabilities)
    response = requests.get('https://api.doordash.com/v2/store_feed/?extra%5Bis_prefetch%5D=false&extra%5BlocationMode%5D=DELIVERY&market_id=132&store_group=78&timezone_offset=-420&tastes%5B%5D=1', proxies=proxy)
    data = response.json()
    if isinstance(data, dict) and data.get('stores'):
        message = 'Your DoorDash orders link has been sent to your email.'
    else:
        message = 'Sorry, we could not retrieve the DoorDash store feed.'

    # Render the result template with the
