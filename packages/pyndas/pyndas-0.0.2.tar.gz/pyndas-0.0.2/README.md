# PYNDAS
Pembelajaran membuat Sebuah Library Python.
Library ini digunakan untuk melakukan proses transformasi data nested array supaya bisa mengumpulkan semua datamenjadi satu. berharap bisa melakukan
preprocessing tidak memakan waktu

## Penggunaan

### Instalasi
Untuk mendownload dan menginstall library ini, gunakan perintah
```sh
pip install pyndas
```


### Pemanggilan
Pemanggilan fungsi bisa dilakukan dengan import sederhana terhadap function yang tersedia
```Python
import pyndas

```
Berikut secara gambaran dari nested array dari sudut pandang format json
```json
{
    "_id": {
      "$oid": ""
    },
    "customer_info": {
      "Cust City Name": "",
      "Cust Province Name": "",
      "Cust Subdistrict Name": ""
    },
    "payment_info": {
      "Payment Method": "",
      "Payment Status": "",
      "Mode": ""
    },
    "order_info": {
      "Order ID": "",
      "User ID": "",
      "Created At": "",
      "Completed At": null,
      "Updated At": "",
      "Total Price": ,
      "Total Product Price": ,
      "Type": ""
    },
    "product_data": {
      "Product ID": null,
      "Product Price": 
    },
    "shipping_data": {
      "Ship ID": "",
      "Ship Cost": null,
      "Weight": null,
      "Courier": null,
      "Delivery Status": "",
      "Shipping Payment": "",
      "Manifested": "",
      "Manifested At": null,
      "Receipt Number": null,
      "Origin ID": "261",
      "Dest ID": "261",
      "Pickup At": null,
      "Shipping Service": null,
      "On Proses Deliver": null,
      "On Proses Return": null
    }
  }

  **OR**

{
  "_id": {
    "$oid": ""
  },
  "user_id": {
    "$oid": ""
  },
  "product_id": {
    "$oid": ""
  },
  "form_id": {
    "$oid": ""
  },
  "is_deleted": false,
  "order_id": ,
  "product_data": {
    "name": "",
    "slug": "",
    "code": "",
    "type": "",
    "price": ,
    "sale_price": {
      "enabled": false,
      "price": 0,
      "schedule": {
        "enabled": true,
        "since": "",
        "until": ""
      }
    },
    "cogs": ,
    "variations": {
      "attributes": [],
      "prices": [],
      "multiple_variations": {
        "enabled": false
      }
    },
    "wholesale": [],
    "picture": ""
  },
  "form_data": {
    "name": ""
  },
  "customer_data": {
    "name": "",
    "phone": "",
    "email": "",
    "notes": "",
    "address": ""
  },
  "product_price": ,
  "product_weight": ,
  "shipping": {
    "courier": "",
    "service": "",
    "cost": 0,
    "cod": false,
    "cod_cost": 0,
    "cod_include_shipping": true,
    "cod_fee_type": "",
    "cod_min": ,
    "cod_max": ,
    "cod_percentage": ,
    "markup": 0,
    "original_cost": 0,
    "origin_id": ,
    "weight": ,
    "mode": ""
  },
  "bump": {
    "checked": false,
    "name": "",
    "price": 0,
    "weight": 1
  },
  "coupon": {
    "id": "",
    "code": "",
    "discount": 0,
    "discount_for": ""
  },
  "total_product_price": ,
  "total_price": ,
  "unique_code_price": {
    "type": "",
    "unique_code": 0
  },
  "cogs": ,
  "progress": {
    "welcome": false,
    "follow_up_1": false,
    "follow_up_2": false,
    "follow_up_3": false,
    "follow_up_4": false,
    "processing": false,
    "closing": false,
    "cancelled": false,
    "up_selling": false
  },
  "progress_sms": {
    "welcome": false,
    "follow_up_1": false,
    "follow_up_2": false,
    "follow_up_3": false,
    "follow_up_4": false,
    "processing": false,
    "closing": false,
    "cancelled": false,
    "up_selling": false
  },
  "payment": {
    "method": "",
    "data": [],
    "channels": [],
    "status": ""
  },
  "status": "",
  "is_printed": false,
  "meta": {
    "url": "",
    "fbc": "",
    "fbp": "",
    "ip": "",
    "os": "",
    "browser": "",
    "location": "",
    "network": "",
    "device_type": "",
    "device_model": "",
    "user_agent": "",
    "embed": false,
    "referrer": "",
    "uuid": ""
  },
  "belongs_to": [
    {
      "$oid": ""
    }
  ],
  "type": "",
  "hash": "",
  "other_cost": 0,
  "dropship": {
    "enabled": false,
    "name": "",
    "phone": ""
  },
  "is_stock_reduced": false,
  "customer_id": {
    "$oid": ""
  },
  "updated_at": {
    "$date": ""
  },
  "created_at": {
    "$date": ""
  }
}

```
### Fungsi Tersedia
1. RemoveRedudancy-data   
2. TransformData-nested_array 

## Changelog:
### v0.1
library masih permulaan, 
1. 
2. 

## Stats


     
License
----
Menggunakan
MIT License
