import asyncio
import random
import traceback
from random import randint

import requests
import re
import time
import json

from app import celery
from crud import customer_crud, answer_crud
from model.customer import Customer
from utils.decorator import get_db, get_db_celery


@celery.task()
@get_db_celery
def crawler(db, customer_id: int):
    p = r'[A-F]'  # 匹配answer
    pattern = re.compile(p)
    with celery.app.app_context():
        customer = customer_crud.get(db, customer_id)
        url = customer.url
        subject_id = customer.subject_id
        total_mark = customer.total_mark
        accuracy = customer.accuracy
        got_mark = customer.got_mark
        print(customer_id)
        headers_1 = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041211AC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 yiban_android',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'qm.linyisong.top',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }
        response_1 = requests.post(url=url, headers=headers_1)
        # print(response_1.text)
        cookies = response_1.cookies.get_dict()
        print(cookies)
        headers_2 = {
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041211AC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 yiban_android',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'qm.linyisong.top',
            'Cookie': 'JSESSIONID=' + cookies['JSESSIONID'] + '; Path=/yiban-web; HttpOnly',
            'Upgrade-Insecure-Requests': '1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        }

        response_2 = requests.post(url=url, headers=headers_2)
        # print(response_2.text)
        cookie = 'JSESSIONID=' + cookies['JSESSIONID']
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 12; 22041211AC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.134 Mobile Safari/537.36 yiban_android',
            'Host': 'qm.linyisong.top',
            'Origin': 'http://qm.linyisong.top',
            'Referer': 'http://qm.linyisong.top/yiban-web/stu/toSubject.jhtml?courseId=' + str(subject_id),
            'Cookie': cookie,
            'Accept': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        question_url = 'http://qm.linyisong.top/yiban-web/stu/nextSubject.jhtml?_=' + str(int(time.time()) * 1000 + randint(0, 1000))
        choice_url = 'http://qm.linyisong.top/yiban-web/stu/changeSituation.jhtml?_=' + str(int(time.time()) * 1000 + randint(0, 1000))

        total_tmp = 1
        now_ = 0
        failed_count = 0
        try:
            while got_mark < total_mark:
                if failed_count >= 20:
                    break
                response = requests.post(url=question_url, data={'courseId': subject_id}, headers=headers)
                print(response.text)
                question_json = response.json()
                uuid = question_json.get('data', {}).get('uuid', '')
                question = question_json.get('data', {}).get('nextSubject', {}).get('subDescript', '')
                answer = answer_crud.get_answer_by_question_subject_id(db, question, subject_id)
                if answer:
                    choice = answer.choice
                else:
                    choice = 'A'
                if (now_ / total_tmp * 100) > accuracy + 2:
                    choice = 'A'
                if '刷题' in question:
                    if random.random() > 0.5:
                        failed_count += 1
                        time.sleep(4)
                        continue
                    else:
                        try:
                            choice = re.search('[A-F]', question).group(0)
                        except:
                            choice = 'C'
                response2 = requests.post(url=choice_url,
                                          data={'answer': choice, 'courseId': subject_id, 'uuid': uuid},
                                          headers=headers)

                answer_json = response2.json()
                is_true = answer_json.get('data', {}).get('rightAnswer', None)
                if is_true is None:
                    print(answer_json)
                    time.sleep(30)
                    continue
                if is_true:
                    true_choice = choice
                    now_ += 1
                    customer_crud.add_got_mark(db, customer_id)
                else:
                    right_option = answer_json.get('data', {}).get('rightOption', '')
                    true_choice_list = re.findall(pattern, right_option)
                    true_choice_list = list(set(true_choice_list))
                    true_choice_list.sort()
                    true_choice = ''.join(true_choice_list)
                    customer_crud.minus_got_mark(db, customer_id)
                data = {
                    'question': question,
                    'choice': true_choice,
                    'subject_id': subject_id
                }
                if '刷题' in question:
                    data['choice'] = choice
                if true_choice != '':
                    answer_crud.create_or_update(db, data)
                got_mark = customer.got_mark
                total_tmp += 1
                time.sleep(8)
            customer_crud.set_real_accuracy(db, customer_id, (now_ / total_tmp * 100))

        except Exception as e:
            traceback.print_exc()
            time.sleep(10)
