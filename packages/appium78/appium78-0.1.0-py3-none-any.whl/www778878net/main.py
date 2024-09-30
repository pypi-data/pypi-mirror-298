from .appium78 import Appium78
import asyncio

async def main():
    # 创建Appium78实例
    appium = Appium78(
        device_name="your_device_name",
        app_package="com.example.app",
        app_activity="com.example.app.MainActivity"
    )

    # 初始化驱动
    appium.initialize_driver()

    # 执行向下滑动
    await appium.perform_swipe_down()

    # 查找元素示例
    elements = appium.find_elements("xpath_or_other_locator")
    for element in elements:
        appium.click_element(element)

    # 获取页面源码
    page_source = appium.get_page_source()
    print(page_source)

    # 获取特定元素的DOM
    element_dom = appium.get_element_dom_by_xpath("//some/xpath")
    print(element_dom)

    # 退出驱动
    appium.quit()

if __name__ == "__main__":
    asyncio.run(main())
