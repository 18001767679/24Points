# -*- encoding : utf-8 -*-
import copy
import json
import os
import random
import re
import time

from khl import Bot, Message, Cert
from khl.card import Card, Types, Module, CardMessage, Element

# webhook
# bot = Bot(cert=Cert(token='token', verify_token='verify_token'), port=3000,
#           route='/khl-wh')

# websocket
bot = Bot(token='token')


# 解法来自于知乎用户 @曲晋云 在 https://zhuanlan.zhihu.com/p/37608401 评论区内的回答
class Solution:
    solutions = set()

    def point24(self, numbers):
        if len(numbers) == 1:
            if abs(eval(numbers[0]) - 24) < 0.00001:
                self.solutions.add(numbers[0])
        else:
            for i in range(len(numbers)):
                for j in range(i + 1, len(numbers)):
                    rest_numbers = [x for p, x in enumerate(numbers) if p != i and p != j]
                    for op in "+-*/":
                        if op in "+-*" or eval(str(numbers[j])) != 0:
                            self.point24(["(" + str(numbers[i]) + op + str(numbers[j]) + ")"] + rest_numbers)
                        if op == "-" or (op == "/" and eval(str(numbers[i])) != 0):
                            self.point24(["(" + str(numbers[j]) + op + str(numbers[i]) + ")"] + rest_numbers)

    def clear(self):
        self.solutions.clear()

    def get_answer(self):
        return self.solutions

    def is_have_answer(self):
        return len(self.solutions) >= 1

    def get_answer_top5_text(self):
        if len(self.solutions) == 0:
            return '无答案'
        answer = ''
        count = 1
        for i in self.solutions:
            answer += f'{i[1:-1]}\n'
            count += 1
            if count >= 6:
                break
        return answer.replace('*', '\\*')


cache = {}
solution_object = Solution()


@bot.command(regex=r'(?:24点自动)')
async def twenty_four_init(msg: Message):
    global cache
    cache_id = f'{msg.ctx.guild.id}-{msg.ctx.channel.id}-{msg.author_id}'
    if cache_id not in cache:
        solution = copy.deepcopy(solution_object)
        await msg.reply(f'.24开始')

@bot.command(regex=r'(?:来一把紧张刺激的 24 点！输入算式进行推导，输入「24退出」结束游戏'))
async def twenty_four_solution(msg: Message):
    global cache
    cache_id = f'{msg.ctx.guild.id}-{msg.ctx.channel.id}-{msg.author_id}'
    if cache_id not in cache:
        solution = copy.deepcopy(solution_object)
        cards = ",".split("]".split("[".split(msg.content)[1])[0])#来一把紧张刺激的 24 点！输入算式进行推导，输入「24退出」结束游戏\n@24点互补 现在你手上有：[7, 6, 12, 13]，怎么凑 24 点呢？
        solution.clear()
        solution.point24(cards)
        await msg.reply(solution.getanswer()[0])



if __name__ == '__main__':
    bot.run()
