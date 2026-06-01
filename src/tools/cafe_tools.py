import unicodedata
from typing import Any, Dict, List, Optional


MENU_CATEGORIES = [
    {
        "name": "CA PHE PHIN",
        "subtitle": "Traditional Coffee",
        "sizes": ["Nho", "Vua", "Lon"],
        "items": [
            {
                "name": "Phin Sua Da",
                "english": "Iced Coffee with Condensed Milk",
                "prices": {"nho": 29000, "vua": 39000, "lon": 45000},
                "stock": 20,
                "aliases": ["ca phe sua", "ca phe sua da", "phin sua da"],
            },
            {
                "name": "Phin Den Da",
                "english": "Iced Black Coffee",
                "prices": {"nho": 29000, "vua": 35000, "lon": 39000},
                "stock": 20,
                "aliases": ["ca phe den", "ca phe den da", "phin den da"],
            },
            {
                "name": "Bac Xiu",
                "english": "Iced White Phin Coffee & Condensed Milk",
                "prices": {"nho": 29000, "vua": 39000, "lon": 45000},
                "stock": 16,
                "aliases": ["bac xiu", "bac siu"],
            },
        ],
    },
    {
        "name": "PHINDI",
        "subtitle": "Traditional Coffee",
        "sizes": ["Nho", "Vua", "Lon"],
        "items": [
            {
                "name": "PhinDi Hanh Nhan",
                "english": "Iced Coffee with Almond & Fresh Milk",
                "prices": {"nho": 45000, "vua": 49000, "lon": 55000},
                "stock": 12,
                "aliases": ["phindi hanh nhan", "hanh nhan"],
            },
            {
                "name": "PhinDi Kem Sua",
                "english": "Iced Coffee with Milk Foam",
                "prices": {"nho": 45000, "vua": 49000, "lon": 55000},
                "stock": 12,
                "aliases": ["phindi kem sua", "kem sua"],
            },
            {
                "name": "PhinDi Choco",
                "english": "Iced Coffee with Chocolate",
                "prices": {"nho": 45000, "vua": 49000, "lon": 55000},
                "stock": 12,
                "aliases": ["phindi choco", "choco"],
            },
        ],
    },
    {
        "name": "TRA",
        "subtitle": "Tea",
        "sizes": ["Nho", "Vua", "Lon"],
        "items": [
            {
                "name": "Tra Sen Vang",
                "english": "Tea with Lotus Seeds",
                "prices": {"nho": 45000, "vua": 55000, "lon": 65000},
                "stock": 10,
                "aliases": ["tra sen vang", "sen vang"],
            },
            {
                "name": "Tra Thach Dao",
                "english": "Tea with Peach Jelly",
                "prices": {"nho": 45000, "vua": 55000, "lon": 65000},
                "stock": 10,
                "aliases": ["tra thach dao", "thach dao"],
            },
            {
                "name": "Tra Thanh Dao",
                "english": "Peach Tea with Lemongrass",
                "prices": {"nho": 45000, "vua": 55000, "lon": 65000},
                "stock": 10,
                "aliases": ["tra dao", "tra thanh dao", "thanh dao"],
            },
            {
                "name": "Tra Thach Vai",
                "english": "Tea with Lychee Jelly",
                "prices": {"nho": 45000, "vua": 55000, "lon": 65000},
                "stock": 10,
                "aliases": ["tra thach vai", "thach vai", "tra vai"],
            },
            {
                "name": "Tra Xanh Dau Do",
                "english": "Green Tea with Red Bean",
                "prices": {"nho": 45000, "vua": 55000, "lon": 65000},
                "stock": 10,
                "aliases": ["tra xanh dau do", "dau do"],
            },
        ],
    },
    {
        "name": "FREEZE",
        "subtitle": "",
        "sizes": ["Nho", "Vua", "Lon"],
        "items": [
            {
                "name": "Freeze Tra Xanh",
                "english": "Green Tea Freeze",
                "prices": {"nho": 55000, "vua": 65000, "lon": 69000},
                "stock": 8,
                "aliases": ["freeze tra xanh", "matcha latte", "tra xanh freeze"],
            },
            {
                "name": "Caramel Phin Freeze",
                "english": "Caramel Phin Freeze",
                "prices": {"nho": 55000, "vua": 65000, "lon": 69000},
                "stock": 8,
                "aliases": ["caramel phin freeze"],
            },
            {
                "name": "Cookies & Cream",
                "english": "Cookies & Cream",
                "prices": {"nho": 55000, "vua": 65000, "lon": 69000},
                "stock": 8,
                "aliases": ["cookies cream", "cookies and cream"],
            },
            {
                "name": "Freeze So-Co-La",
                "english": "Chocolate Freeze",
                "prices": {"nho": 55000, "vua": 65000, "lon": 69000},
                "stock": 8,
                "aliases": ["freeze socola", "freeze so co la", "chocolate freeze"],
            },
            {
                "name": "Classic Phin Freeze",
                "english": "Classic Phin Freeze",
                "prices": {"nho": 55000, "vua": 65000, "lon": 69000},
                "stock": 8,
                "aliases": ["classic phin freeze"],
            },
        ],
    },
    {
        "name": "BANH",
        "subtitle": "Pastry",
        "sizes": [],
        "items": [
            {"name": "Banh Chuoi", "english": "Banana Cake", "prices": {"one_size": 29000}, "stock": 10, "aliases": ["banh chuoi"]},
            {"name": "Pho Mai Chanh Day", "english": "Passion Fruit Cheese Cake", "prices": {"one_size": 29000}, "stock": 10, "aliases": ["pho mai chanh day"]},
            {"name": "Banh Su Kem", "english": "Cream Choux", "prices": {"one_size": 29000}, "stock": 10, "aliases": ["banh su kem"]},
            {"name": "Tiramisu", "english": "Tiramisu Cake", "prices": {"one_size": 35000}, "stock": 10, "aliases": ["tiramisu"]},
            {"name": "Mousse Dao", "english": "Peach Mousse", "prices": {"one_size": 35000}, "stock": 10, "aliases": ["mousse dao"]},
            {"name": "Mousse Cacao", "english": "Cocoa Mousse", "prices": {"one_size": 35000}, "stock": 10, "aliases": ["mousse cacao"]},
            {"name": "Pho Mai Tra Xanh", "english": "Green Tea Cheese Cake", "prices": {"one_size": 35000}, "stock": 10, "aliases": ["pho mai tra xanh"]},
            {"name": "Pho Mai Caramel", "english": "Caramel Cheese Cake", "prices": {"one_size": 35000}, "stock": 10, "aliases": ["pho mai caramel"]},
            {"name": "So-Co-La Highlands", "english": "Chocolate Highlands Cake", "prices": {"one_size": 35000}, "stock": 10, "aliases": ["socola highlands", "so co la highlands"]},
            {"name": "Sua Chua Pho Mai", "english": "Yogurt Cheese", "prices": {"one_size": 39000}, "stock": 10, "aliases": ["sua chua pho mai"]},
        ],
    },
    {
        "name": "BANH MI QUE",
        "subtitle": "Breadsticks",
        "sizes": [],
        "items": [
            {"name": "Pate", "english": "Pate", "prices": {"one_size": 19000}, "stock": 18, "aliases": ["pate", "banh mi que pate"]},
            {"name": "Ga Pho Mai", "english": "Chicken & Cheese", "prices": {"one_size": 19000}, "stock": 18, "aliases": ["ga pho mai", "banh mi que ga pho mai"]},
            {"name": "Bo Sot Pho Mai", "english": "Beef Breadsticks with Cheese Sauce", "prices": {"one_size": 25000}, "stock": 18, "aliases": ["bo sot pho mai", "banh mi que bo sot pho mai"]},
        ],
    },
    {
        "name": "COMBO",
        "subtitle": "",
        "sizes": ["Nho", "Vua", "Lon"],
        "items": [
            {
                "name": "Hung Khoi",
                "english": "Phin Sua Da & Banh Mi Que",
                "prices": {"nho": 39000, "vua": 47000, "lon": 49000},
                "stock": 10,
                "aliases": ["hung khoi", "combo hung khoi"],
            },
            {
                "name": "Chuyen Tro",
                "english": "Tra & Banh Ngot",
                "prices": {"nho": 69000, "vua": 75000, "lon": 79000},
                "stock": 10,
                "aliases": ["chuyen tro", "combo chuyen tro"],
            },
        ],
    },
]


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
    text = text.replace("&", " and ")
    return " ".join(text.lower().strip().split())


def _build_menu_index() -> Dict[str, Dict[str, Any]]:
    index = {}
    for category in MENU_CATEGORIES:
        for item in category["items"]:
            indexed_item = {**item, "category": category["name"]}
            keys = [item["name"], item["english"], *item.get("aliases", [])]
            for key in keys:
                index[_normalize(key)] = indexed_item
    return index


MENU = _build_menu_index()

CATEGORY_ALIASES = {
    "banh mi": "BANH MI QUE",
    "banh mi que": "BANH MI QUE",
    "breadstick": "BANH MI QUE",
    "breadsticks": "BANH MI QUE",
    "banh": "BANH",
    "banh ngot": "BANH",
    "pastry": "BANH",
    "pastries": "BANH",
}


def _normalize_size(size: Optional[str], prices: Dict[str, int]) -> str:
    requested = _normalize(size or "")
    size_aliases = {
        "small": "nho",
        "s": "nho",
        "nho": "nho",
        "medium": "vua",
        "m": "vua",
        "vua": "vua",
        "large": "lon",
        "l": "lon",
        "lon": "lon",
        "one size": "one_size",
        "one_size": "one_size",
    }
    normalized = size_aliases.get(requested)
    if normalized in prices:
        return normalized
    if "nho" in prices:
        return "nho"
    if "one_size" in prices:
        return "one_size"
    return next(iter(prices))


def _get_category_options(category_name: str) -> List[Dict[str, Any]]:
    for category in MENU_CATEGORIES:
        if category["name"] == category_name:
            options = []
            for item in category["items"]:
                prices = item["prices"]
                if "one_size" in prices:
                    price_text = {"one_size": prices["one_size"]}
                else:
                    price_text = {size: prices[size] for size in ["nho", "vua", "lon"]}
                options.append(
                    {
                        "item_name": item["name"],
                        "english": item["english"],
                        "prices": price_text,
                        "stock": item["stock"],
                        "available": item["stock"] > 0,
                    }
                )
            return options
    return []


def get_menu_item(item_name: str, size: Optional[str] = None) -> Dict[str, Any]:
    """Return price and stock status for one menu item."""
    key = _normalize(item_name)
    item = MENU.get(key)
    if not item:
        category_name = CATEGORY_ALIASES.get(key)
        if category_name:
            return {
                "found": True,
                "ambiguous": True,
                "category": category_name,
                "item_name": item_name,
                "message": "This is a menu category. Ask the user to choose one specific item.",
                "options": _get_category_options(category_name),
            }

        return {
            "found": False,
            "item_name": item_name,
            "message": "Item is not on the cafe menu.",
        }

    selected_size = _normalize_size(size, item["prices"])
    price = item["prices"][selected_size]

    return {
        "found": True,
        "item_name": item["name"],
        "english": item["english"],
        "category": item["category"],
        "size": selected_size,
        "price": price,
        "prices": item["prices"],
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
            "description": (
                "Look up one cafe menu item by name. Optional size accepts nho, vua, lon. "
                "Returns selected price, all prices, stock, and availability. "
                "If the input is a category such as banh mi, banh mi que, breadstick, or banh, "
                "returns ambiguous=true with options instead of saying the item is missing."
            ),
            "args_schema": {"item_name": "string", "size": "string optional: nho | vua | lon"},
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
