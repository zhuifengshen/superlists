from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
import time
from functional_tests.base import FunctionalTest


class NewVisitorTest(FunctionalTest):
    def test_can_start_a_list_and_retrieve_it_later(self):
        # 伊迪丝听说有一个很酷的在线待办事项应用
        # 她去看了这个应用的首页
        self.browser.get(self.server_url)
        # 她注意到网页的标题和头部都包含“To-Do”这个词
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # 应用邀请她输入一个待办事项
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), 'Enter a to-do item')
        # 她在一个文本框中输入了“Buy peacock feathers(”购买孔雀羽毛)
        # 伊迪丝的爱好是使用假蝇做饵钓鱼
        inputbox.send_keys('Buy peacock feathers')

        # 她按回车键后，被带到了一个新URL
        # 这个页面的待办事项清单中显示了“Buy peacock feathers”
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)  # 通过暂停，以便浏览器渲染页面
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        # table = self.browser.find_element_by_id('id_list_table')  # 元素不存在，则抛出异常
        # rows = table.find_elements_by_tag_name('tr')  # 元素不存在，返回一个空列表
        # self.assertTrue(any(row.text == '1: Buy peacock feathers' for row in rows), "New to-do item did not appear in table")
        # self.assertIn('1:Buy peacock feathers', [row.text for row in rows])
        # time.sleep(1)  # selenium.common.exception.StaleElementReferenceException: Message: The element reference of <table id="id_list_table"> is stale.
        WebDriverWait(self.browser, 10).until(expected_conditions.text_to_be_present_in_element((By.ID, 'id_list_table'), '1: Buy peacock feathers'))
        self.check_for_row_in_list_table('1: Buy peacock feathers')

        # 页面中又显示了一个文本框，可以输入其他的待办事项
        # 她输入了“Use peacock feathers to make a fly(”使用孔雀羽毛做假蝇)
        # 伊迪丝做事很有条理
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        time.sleep(1)
        inputbox.send_keys(Keys.ENTER)

        # 页面再次更新，她的清单中显示了这两个待办事项
        # table = self.browser.find_element_by_id('id_list_table')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertIn('1:Buy peacock feathers', [row.text for row in rows])
        # self.assertIn('2:Use peacock feathers to make a fly', [row.text for row in rows])
        time.sleep(1)
        self.check_for_row_in_list_table('1: Buy peacock feathers')
        self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')
        # 伊迪丝想知道这个网站是否会记住她的清单
        # 她看到网站为她生成了一个唯一的URL
        # 而且页面中有一些文字解说这个功能
        # self.fail('Finish the test!')
        # 她访问那个URL，发现她的待办事项列表还在
        # 她很满意，去睡觉了

        # 现在一个叫费朗西斯的新用户访问了网站

        ## 我们使用一个新浏览器会话
        ## 确保伊迪丝的信息不会从cookie中泄露
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # 弗朗西斯访问首页
        # 页面中看不到伊迪丝的清单
        self.browser.get(self.server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('Use peacock feathers to make a fly', page_text)

        # 弗朗西斯输入一个新待办事项，新建一个清单
        # 他不想伊迪丝那样兴趣盎然
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

        # 弗朗西斯获得了他唯一URL
        time.sleep(1)
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 这个页面还是没有伊迪丝的清单
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 两人都很满意，去睡觉了