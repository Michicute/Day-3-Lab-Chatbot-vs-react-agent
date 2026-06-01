import unicodedata
from typing import Any, Dict, List


MENU = {
    "ca phe sua": {"display_name": "ca phe sua", "price": 30000, "stock": 10},
    "tra dao": {"display_name": "tra dao", "price": 45000, "stock": 5},
    "matcha latte": {"display_name": "matcha latte", "price": 55000, "stock": 0},
}

COUPONS = {
    "GIAM10": {"type": "percent", "value": 0.10},
    "FREESHIP": {"type": "free_shipping", "value": 1.0},
}

DELIVERY_FEES = {
    "quan 1": 15000,
    "quan 3": 20000,
    "quan 7": 30000,
}


def _normalize(value: str) -> str:
    text = unicodedata.normalize("NFKD", str(value or ""))
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.replace("đ", "d").replace("Đ", "D")
    return " ".join(text.lower().strip().split())


def get_menu_item(item_name: str) -> Dict[str, Any]:
    """Return price and stock status for one menu item."""
    key = _normalize(item_name)
    item = MENU.get(key)
    if not item:
        return {
            "found": False,
            "item_name": item_name,
            "message": "Item is not on the cafe menu.",
        }

    return {
        "found": True,
        "item_name": item["display_name"],
        "price": item["price"],
        "stock": item["stock"],
        "available": item["stock"] > 0,
    }


def apply_coupon(coupon_code: str, subtotal: float, delivery_fee: float = 0) -> Dict[str, Any]:
    """Apply a coupon to the order subtotal or delivery fee."""
    code = _normalize(coupon_code).upper()
    coupon = COUPONS.get(code)
    if not coupon:
        return {
            "valid": False,
            "coupon_code": coupon_code,
            "discount_amount": 0,
            "delivery_discount": 0,
            "message": "Coupon is invalid.",
        }

    if coupon["type"] == "percent":
        discount_amount = int(float(subtotal) * coupon["value"])
        return {
            "valid": True,
            "coupon_code": code,
            "discount_amount": discount_amount,
            "delivery_discount": 0,
            "message": f"Coupon {code} gives {int(coupon['value'] * 100)}% off subtotal.",
        }

    if coupon["type"] == "free_shipping":
        delivery_discount = int(float(delivery_fee))
        return {
            "valid": True,
            "coupon_code": code,
            "discount_amount": 0,
            "delivery_discount": delivery_discount,
            "message": f"Coupon {code} removes the delivery fee.",
        }

    return {
        "valid": False,
        "coupon_code": coupon_code,
        "discount_amount": 0,
        "delivery_discount": 0,
        "message": "Coupon type is unsupported.",
    }


def calc_delivery_fee(district: str) -> Dict[str, Any]:
    """Return delivery fee for a supported district."""
    key = _normalize(district)
    fee = DELIVERY_FEES.get(key)
    if fee is None:
        return {
            "supported": False,
            "district": district,
            "fee": None,
            "message": "Delivery is not supported for this district.",
        }

    return {
        "supported": True,
        "district": key,
        "fee": fee,
    }


def calculate_total(
    subtotal: float,
    discount_amount: float = 0,
    delivery_fee: float = 0,
    delivery_discount: float = 0,
) -> Dict[str, Any]:
    """Calculate the final order total."""
    subtotal = int(float(subtotal))
    discount_amount = int(float(discount_amount))
    delivery_fee = int(float(delivery_fee))
    delivery_discount = int(float(delivery_discount))
    payable_delivery = max(0, delivery_fee - delivery_discount)
    total = max(0, subtotal - discount_amount) + payable_delivery

    return {
        "subtotal": subtotal,
        "discount_amount": discount_amount,
        "delivery_fee": delivery_fee,
        "delivery_discount": delivery_discount,
        "payable_delivery": payable_delivery,
        "total": total,
    }


def get_cafe_tools() -> List[Dict[str, Any]]:
    return [
        {
            "name": "get_menu_item",
            "description": "Look up one cafe menu item by name. Returns price, stock, and availability.",
            "args_schema": {"item_name": "string"},
            "func": get_menu_item,
        },
        {
            "name": "apply_coupon",
            "description": "Apply coupon GIAM10 or FREESHIP. Requires subtotal. FREESHIP also needs delivery_fee.",
            "args_schema": {"coupon_code": "string", "subtotal": "number", "delivery_fee": "number optional"},
            "func": apply_coupon,
        },
        {
            "name": "calc_delivery_fee",
            "description": "Calculate delivery fee for quan 1, quan 3, or quan 7.",
            "args_schema": {"district": "string"},
            "func": calc_delivery_fee,
        },
        {
            "name": "calculate_total",
            "description": "Calculate final total from subtotal, discount_amount, delivery_fee, and delivery_discount.",
            "args_schema": {
                "subtotal": "number",
                "discount_amount": "number optional",
                "delivery_fee": "number optional",
                "delivery_discount": "number optional",
            },
            "func": calculate_total,
        },
    ]
