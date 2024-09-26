import unittest
from pyndas.transform import DataTransformer

class TestDataTransformer(unittest.TestCase):
    def test_flatten(self):
        transformer = DataTransformer()
        data = {
            "_id": {"$oid": "66aad000ee0ec8b58703eedb"},
            "user_id": {"$oid": "643618b1480bd56c700cfbff"},
            "product_id": {"$oid": "6437ce873dcca75a6604d9d4"},
            "form_id": {"$oid": "6437ce873dcca75a6604d9d5"},
            "is_deleted": False,
            "order_id": 205053644,
            "product_data": {
                "name": "Reseller Kremo Kids(11)",
                "slug": "Reseller-KremoKids-11",
                "price": 99000,
                "sale_price": {
                    "enabled": False,
                    "price": 0,
                    "schedule": {
                        "enabled": True,
                        "since": "13-04-2023 00:00:01",
                        "until": "13-04-2023 23:59:59"
                    }
                },
            },
            "customer_data": {
                "name": "Muhyidin",
                "phone": "+6285655425255",
            },
            "payment": {
                "method": "bank_transfer",
                "status": "unpaid"
            },
            "meta": {
                "url": "kremokids.orderonline.id",
                "ip": "114.10.154.158",
                "os": "Android",
            },
            "created_at": {"$date": "2024-08-01T00:00:00.000Z"}
        }
        
        expected = {
            "_id_$oid": "66aad000ee0ec8b58703eedb",
            "user_id_$oid": "643618b1480bd56c700cfbff",
            "product_id_$oid": "6437ce873dcca75a6604d9d4",
            "form_id_$oid": "6437ce873dcca75a6604d9d5",
            "is_deleted": False,
            "order_id": 205053644,
            "product_data_name": "Reseller Kremo Kids(11)",
            "product_data_slug": "Reseller-KremoKids-11",
            "product_data_price": 99000,
            "product_data_sale_price_enabled": False,
            "product_data_sale_price_price": 0,
            "product_data_sale_price_schedule_enabled": True,
            "product_data_sale_price_schedule_since": "13-04-2023 00:00:01",
            "product_data_sale_price_schedule_until": "13-04-2023 23:59:59",
            "customer_data_name": "Muhyidin",
            "customer_data_phone": "+6285655425255",
            "payment_method": "bank_transfer",
            "payment_status": "unpaid",
            "meta_url": "kremokids.orderonline.id",
            "meta_ip": "114.10.154.158",
            "meta_os": "Android",
            "created_at_$date": "2024-08-01T00:00:00.000Z"
        }
        
        # Assert that flatten function works as expected
        self.assertEqual(transformer._flatten(data), expected)

if __name__ == "__main__":
    unittest.main()
