#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : x
# @Time         : 2024/9/20 17:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :
import pandas as pd

from meutils.pipe import *
d = {
    "type": 7,
    "dateStr": "17:34",
    "date": 1726824850010,
    "qaId": "9750204BC4E24EA8835F954371EBC495",
    "sessionId": "7a4b14ca5506b23cde906fa3ea95a9859853c7f4c289f2e3c0179a828cd4ad22b8af4384c5b6b7c52f99dd9e97e1d63c",
    "userId": "fnopsrzxqocuvcfmcppdciqnxyascnla",
    "identify": None,
    "talk": "gpt",
    "data": {
        "question": "法院可以根据当事人的申请对于哪些案件可以裁定先予执行？",
        "useful": 1,
        "showLawQaButton": True,
        "lawQaText": "**结论**：\n法院可以根据当事人的申请，对特定类型的案件裁定先予执行。这些案件主要包括追索赡养费、扶养费、抚养费、抚恤金、医疗费用的案件，追索劳动报酬的案件，以及因情况紧急需要先予执行的案件。\n\n**最适用法规法条**：\n<a onclick=\"onLaws_detail(this,'98829421c8a0397269e2754473e642a8')\">《中华人民共和国民事诉讼法(2023修正)》</a><a onclick=\"onLaws_detail(this,'98829421c8a0397269e2754473e642a8:109')\">第一百零九条</a>\n\n**匹配度**：\n该法条直接回答了用户的问题，明确列出了法院可以根据当事人申请裁定先予执行的案件类型，与用户问题的需求高度匹配。\n\n**理由**：\n根据<a onclick=\"onLaws_detail(this,'98829421c8a0397269e2754473e642a8')\">《中华人民共和国民事诉讼法(2023修正)》</a><a onclick=\"onLaws_detail(this,'98829421c8a0397269e2754473e642a8:109')\">第一百零九条</a>的规定，法院在受理案件时，对于涉及追索赡养费、扶养费、抚养费、抚恤金、医疗费用，追索劳动报酬，以及因情况紧急需要先予执行的案件，可以根据当事人的申请裁定先予执行。这些案件类型通常涉及到当事人的基本生活权益或紧急需求，因此法律赋予了法院在判决前先行作出执行裁定的权力，以保障当事人的合法权益得到及时有效的维护。",
        "lawQaRelatedLaws": [
            {
                "lawId": "98829421c8a0397269e2754473e642a8",
                "articleNum": 109,
                "title": "中华人民共和国民事诉讼法(2023修正)",
                "articleTag": "第一百零九条",
                "articleContent": "人民法院对下列案件，根据当事人的申请，可以裁定先予执行：  （一）追索赡养费、扶养费、抚养费、抚恤金、医疗费用的；  （二）追索劳动报酬的；  （三）因情况紧急需要先予执行的。"
            },
            {
                "lawId": "98829421c8a0397269e2754473e642a8",
                "articleNum": 110,
                "title": "中华人民共和国民事诉讼法(2023修正)",
                "articleTag": "第一百一十条",
                "articleContent": "人民法院裁定先予执行的，应当符合下列条件：  （一）当事人之间权利义务关系明确，不先予执行将严重影响申请人的生活或者生产经营的；  （二）被申请人有履行能力。  人民法院可以责令申请人提供担保，申请人不提供担保的，驳回申请。申请人败诉的，应当赔偿被申请人因先予执行遭受的财产损失。"
            },
            {
                "lawId": "b01aacc56af9ada97a650a2b5394a554",
                "articleNum": 11,
                "title": "最高人民法院司法部关于民事诉讼法律援助工作的规定",
                "articleTag": "第十一条",
                "articleContent": "法律援助案件的受援人依照民事诉讼法的规定申请先予执行，人民法院裁定先予执行的，可以不要求受援人提供相应的担保。"
            }
        ],
        "lawQaRelatedCases": [
            {
                "caseId": "2022D02082640A3FD34151A106016",
                "title": "赵雅婷、王金彪其他案由首次执行执行裁定书",
                "causeName": "执行案件",
                "courtName": "平原县人民法院",
                "caseNo": "（2022）鲁1426执547号",
                "judgeDate": "2022-05-12",
                "viewPoint": "人民法院关于适用〈中华人民共和国民事诉讼法〉的解释》第四百八十五条规定，裁定如下："
            },
            {
                "caseId": "2022938BE182CCF9470251A106016",
                "title": "翁慧琴、李再明民事执行实施类执行裁定书",
                "causeName": "执行案件",
                "courtName": "建德市人民法院",
                "caseNo": "（2022）浙0182执796号",
                "judgeDate": "2022-04-29",
                "viewPoint": "的解释》第四百六十四条规定，裁定如下："
            },
            {
                "caseId": "2021D519163D5B6F3E0C51A106016",
                "title": "赖明春、丁爱琴民事执行实施类执行裁定书",
                "causeName": "执行案件",
                "courtName": "开化县人民法院",
                "caseNo": "（2021）浙0824执1741号之一",
                "judgeDate": "2022-01-24",
                "viewPoint": "的解释》第四百六十六条之规定，裁定如下："
            }
        ],
        "showViewpointQaButton": True,
        "viewpointQaText": None,
        "viewpointQaRelatedArticles": None,
        "showRelatedCaseButton": False,
        "relatedCases": None,
        "showRegulationsButton": False,
        "regulations": None
    }
}

print(pd.DataFrame(d['data']['lawQaRelatedLaws']))

print(pd.DataFrame(d['data']['lawQaRelatedCases']))