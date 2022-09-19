from selenium import webdriver
from selenium.webdriver.common.by import By
import traceback
from datetime import datetime
from selenium.webdriver.support.select import Select
import pdb
import time
import os
from tqdm import trange
import random
from check_availability import get_availability

# 打开一个页面，添加购物车
def open_store(driver):
    # 访问测试的url定义
    url = "https://www.apple.com.cn/shop/buy-iphone/iphone-14-pro"
    driver.get(url)
    # 4. 开始选择规格【此处我选择了-14 pro】
    element_sku = driver.find_elements(By.NAME, 'dimensionScreensize')[1]
    element_sku.click()
    # 4.2 选择颜色【此处我选择了-银色】
    element_color = driver.find_element(By.XPATH,
                                        '//*[@value="deeppurple"]')
    driver.execute_script("arguments[0].click();", element_color)
    # 4.3 选择内存【此处我选择了-256g】
    element_memory = driver.find_element(By.XPATH,
                                         '//*[@value="256gb"]')
    driver.execute_script("arguments[0].click();", element_memory)
    # 4.4 你是否有智能手机要折抵 【此处我选择了-没有旧机折扣】
    element_old = driver.find_element(By.XPATH, '//*[@id="noTradeIn"]')
    driver.execute_script("arguments[0].click();", element_old)
    # 4.5 Applecare 【此处我选择了-无Applecare】
    element_care = driver.find_element(By.ID, 'iphone11promax_ac_iup_noapplecare')
    driver.execute_script("arguments[0].click();", element_care)
    # 4.6 添加到购物袋
    # element_car = driver.find_element(By.XPATH,
    #                                   '//*[@value="add-to-cart"]')
    # driver.execute_script("arguments[0].click();", element_car)
    element_car = driver.find_element(By.NAME,
                                      "add-to-cart")
    driver.execute_script("arguments[0].click();", element_car)

    # 5 页面跳转查看购物袋
    element_check = driver.find_element(By.XPATH,
                                        '//*[@value="proceed"]')
    driver.execute_script("arguments[0].click();", element_check)
    # 6 结账
    element_check_out = driver.find_element(By.XPATH,
                                            '//*[@id="shoppingCart.actions.checkout"]')
    driver.execute_script("arguments[0].click();", element_check_out)
    # 7.1 输入用户名
    element_username = driver.find_element(By.ID,
                                           'signIn.customerLogin.appleId')
    element_username.send_keys('18810929956')

    # 7.2 输入密码
    element_password = driver.find_element(By.ID,
                                           'signIn.customerLogin.password')
    element_password.send_keys('Dxer98711')

    # 7.3 点击登录
    element_login = driver.find_element(By.ID,'signin-submit-button')
    element_login.click()
    # 8.1 你希望如何收到订单商品  【此处我选择了-我要取货】
    element_want_order = driver.find_element(By.ID,
                                             'fulfillmentOptionButtonGroup1')
    driver.execute_script("arguments[0].click();", element_want_order)

    # 如果点击完取货按钮


def refresh_nearby(driver):
    # display_nearby = driver.find_elements(By.CLASS_NAME,
    #                                       "rs-edit-location-button as-buttonlink icon icon-after icon-chevrondown")

    while True:
        # 寻找打开城市按钮
        select_location = driver.find_elements(By.XPATH,
                                           '//*[@class="rs-edit-location-button as-buttonlink icon icon-after icon-chevrondown"]')
        # 如果还没有打开
        if select_location:
            driver.execute_script("arguments[0].click();", select_location[0])
            time.sleep(1)
        else:
            break
    # 最多尝试10下
    rand = ["海淀区", "东城区", "西城区", "丰台区", "朝阳区"]
    area = random.choice(rand)
    for i in range(5):
        selectprovice = driver.find_elements(By.XPATH, "//button[contains(text(),'北京')]")
        for b in selectprovice:
            if b.text == "北京":
                driver.execute_script("arguments[0].click();", b)
        selectarea = driver.find_elements(By.XPATH, "//button[contains(text(),'" + area + "')]")
        for b in selectarea:
            if b.text == area:
                driver.execute_script("arguments[0].click();", b)
        # 如果选择地区按钮关闭了，说明刷新成功
        select_location = driver.find_elements(By.XPATH,
                                               '//*[@class="rs-edit-location-button as-buttonlink icon icon-after icon-chevrondown"]')
        if select_location:
            return 0
    return -1


def fulfill_information(driver):
    print("开始抢！！！！")
    element_pickupTab = driver.find_element(By.XPATH,
                                            '//*[@class="rt-storelocator-store-list"]/fieldset/ul/li[1]/input')
    driver.execute_script("arguments[0].click();", element_pickupTab)

    # 8.8 选择取货时间 【根据时间自己定】
    try:
        element_pickup_time = driver.find_element(By.XPATH,
                                                  '//*[@value="19"]')
        driver.execute_script("arguments[0].click();", element_pickup_time)
    except:
        element_pickup_time = driver.find_element(By.XPATH,
                                                  '//*[@value="20"]')
        driver.execute_script("arguments[0].click();", element_pickup_time)

    # 8.9 选择取货时间段 【此处我选择了-默认第一个时间段】
    element_time_quantum = driver.find_element(By.XPATH,
                                               '//*[@id="checkout.fulfillment.pickupTab.pickup.timeSlot.dateTimeSlots.timeSlotValue"]')
    Select(element_time_quantum).select_by_index(1)

    # 8.10 继续填写取货详情
    element_checkout = driver.find_element(By.ID,
                                           'rs-checkout-continue-button-bottom')
    driver.execute_script("arguments[0].click();", element_checkout)
    element_checkout.click()

    # 9.1 请填写姓氏
    lastName = driver.find_element(By.ID,
                                   'checkout.pickupContact.selfPickupContact.selfContact.address.lastName')
    lastName.send_keys('聂')

    # 9.2 请填写名字
    firstName = driver.find_element(By.ID,
                                    'checkout.pickupContact.selfPickupContact.selfContact.address.firstName')
    firstName.send_keys('振源')

    # # 9.3 请填写电子邮件
    # emailAddress = driver.find_element(By.ID,
    #                                    'checkout.pickupContact.selfPickupContact.selfContact.address.emailAddress')
    # emailAddress.send_keys('dxer@pku.edu.cn')
    # driver.implicitly_wait(10)

    # 9.4 请填写手机号
    emailAddress = driver.find_element(By.ID,
                                       'checkout.pickupContact.selfPickupContact.selfContact.address.fullDaytimePhone')
    emailAddress.send_keys('18810929956')

    # 9.5 请填写身份证后四位
    nationalIdSelf = driver.find_element(By.ID,
                                         'checkout.pickupContact.selfPickupContact.nationalIdSelf.nationalIdSelf')
    nationalIdSelf.send_keys('181X')

    # 选择发票
    element_invoice = driver.find_elements(By.NAME, "checkout.pickupContact.eFapiaoSelector.selectFapiao")[1]
    element_invoice.click()

    # 9.6 继续选择付款方式
    element_checkoutPay = driver.find_element(By.ID,
                                              'rs-checkout-continue-button-bottom')
    driver.execute_script("arguments[0].click();", element_checkoutPay)

    # 10 立即下单 【此处我选择了-微信支付】
    element_billingOptions = driver.find_element(By.ID,
                                                 'checkout.billing.billingoptions.wechat_label')
    driver.execute_script("arguments[0].click();", element_billingOptions)

    # 11.1 确定
    element_orderPay = driver.find_element(By.ID,
                                           'rs-checkout-continue-button-bottom')
    driver.execute_script("arguments[0].click();", element_orderPay)

    # 12 确认订单
    element_endPay = driver.find_element(By.ID,
                                         'rs-checkout-continue-button-bottom')
    driver.execute_script("arguments[0].click();", element_endPay)

    for _ in range(5):
        # 有可能会卡，多按几次按钮
        try:
            element_endPay = driver.find_element(By.ID,
                                                 'rs-checkout-continue-button-bottom')
            driver.execute_script("arguments[0].click();", element_endPay)
        except:
            break

    time.sleep(60)


def main(driver):
    driver.implicitly_wait(1)
    while True:
        try:
            open_store(driver)
            break
        except:
            continue
    isOK=False
    refresh_nearby(driver)
    stores = driver.find_elements(By.XPATH, '//*[@class="rt-storelocator-store-list"]/fieldset/ul/li[1]/input')
    if stores:
        isOK = stores[0].is_enabled()
    else:
        try:
            driver.find_element(By.XPATH, "//span[contains(text(),'继续填写取货详情')]")
        except:
            return -1
    if not isOK:
        for _ in trange(200):
            # 检查库存，5分钟后刷新页面
            available=get_availability()
            if not available:
                time.sleep(1)
                continue
            # 刷新5次
            for _ in range(5):
                r = refresh_nearby(driver)
                stores = driver.find_elements(By.XPATH, '//*[@class="rt-storelocator-store-list"]/fieldset/ul/li[1]/input')
                if stores:
                    isOK = stores[0].is_enabled()
                else:
                    continue
                if isOK:
                    break
            break
    driver.implicitly_wait(5)
    if isOK:
        for _ in range(10):
            try:
                fulfill_information(driver)
            except:
                refresh_nearby(driver)
                traceback.print_exc()
    return 0


if __name__ == '__main__':
    counter = 1
    options = webdriver.ChromeOptions()
    # options.add_argument('blink-settings=imagesEnabled=false')
    while True:
        print("第%d次尝试" % counter)
        try:
            driver.quit()
        except:
            pass
        driver = webdriver.Chrome()
        # driver.minimize_window()
        try:
            main(driver)
        except:
            traceback.print_exc()
            driver.quit()
        counter += 1
