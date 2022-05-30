from pprint import pprint
from notion_client import Client
import datetime
import os

class NotionHelper:
    notion = None

    def __init__(self):
        self.notion = Client(auth=os.environ['NOTION_TOKEN'])

    def get_discord_list(self, list_id):
        return self.notion.databases.query(
            **{
                'database_id' : list_id,
            }
        )

    def get_notpaid(self, database_id):
        return self.notion.databases.query(
            **{
                'database_id' : database_id,  # データベースID,
                'filter': {
                    'or' :[
                        {
                            'and':[
                            {
                                'property': "付款狀況",
                                'select': {
                                'equals': "尚未付款"
                                }
                            },{
                                'property': "建立時間",
                                'created_time':{
                                    'before': (datetime.date.today() - datetime.timedelta(days=60)).strftime("%Y-%m-%d")
                                }
                            }
                            ]
                        },{
                            'and':[
                            {
                                'property': "付款狀況",
                                'select': {
                                    'equals': "尚未付款"
                                }
                            },{
                                'property': "台幣",
                                'number':{
                                    'less_than': 0
                                }
                            }
                            ]
                        }
                    ]
                }
            } 
        )   