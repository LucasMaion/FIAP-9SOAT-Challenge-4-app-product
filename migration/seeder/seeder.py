from decimal import Decimal
from typing import List, Tuple
from faker import Faker


from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.product_components import ProductComponent
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.select_product import SelectedProduct
from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)

fake = Faker("pt_BR")


def _seed_category() -> List[int]:
    bebidas = Category(
        name="Bebidas",
        description="Bebidas refrigerantes, sucos, água, etc.",
        is_component=False,
    )
    bebidas.save()
    lanches = Category(
        name="Lanches",
        description="Lanches e produtos principais",
        is_component=False,
    )
    lanches.save()
    acompanhamentos = Category(
        name="Acompanhamentos",
        description="Batatas fritas, nuggets, etc.",
        is_component=False,
    )
    acompanhamentos.save()
    adicionais = Category(
        name="Adicionais",
        description="Queijo, bacon, hambúrguer, etc.",
        is_component=True,
    )
    adicionais.save()
    return [bebidas.id, lanches.id, acompanhamentos.id, adicionais.id]


def _seed_currency() -> int:
    currency = Currency(
        symbol="R$",
        name="Real",
        code="BRL",
        is_active=True,
    )
    currency.save()
    return currency.id


def _seed_product_and_product_components(
    bebida_id: List[int], lanche_id: int, acompanhamento_id: int, adicional_id: int
) -> Tuple[List[int], List[List[int]]]:

    big = Product(
        name="Big Lanche",
        description="big lanchinho",
        price=Decimal(27.90),
        category=lanche_id,
        allow_components=True,
        is_active=True,
        currency=1,
    )
    big.save()
    chester_b = Product(
        name="Chester Burger",
        description="diferentão",
        price=Decimal(32.90),
        category=lanche_id,
        allow_components=True,
        is_active=True,
        currency=1,
    )
    chester_b.save()
    cocorico = Product(
        name="Cocoricó",
        description="franguinho",
        price=Decimal(22.90),
        category=lanche_id,
        allow_components=True,
        is_active=True,
        currency=1,
    )
    cocorico.save()
    fritas = Product(
        name="Fritas",
        description="fritinhas",
        price=Decimal(12.90),
        category=acompanhamento_id,
        is_active=True,
        currency=1,
    )
    fritas.save()
    fritas_special = Product(
        name="Fritas Special",
        description="fritinhas",
        price=Decimal(12.90),
        category=acompanhamento_id,
        is_active=False,
        currency=1,
    )
    fritas_special.save()
    nuggets = Product(
        name="nuggets",
        description=fake.sentence(),
        price=fake.random_number(2),
        category=acompanhamento_id,
        is_active=True,
        currency=1,
    )
    nuggets.save()
    doll = Product(
        name="doll cola",
        description="refri",
        price=Decimal(5.90),
        category=bebida_id,
        is_active=True,
        currency=1,
    )
    doll.save()
    sukinho = Product(
        name="sukinho",
        description="suco",
        price=Decimal(4.90),
        category=bebida_id,
        is_active=True,
        currency=1,
    )
    sukinho.save()
    hambuguer = Product(
        name="hambuguer",
        price=Decimal(5),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    hambuguer.save()
    chicken = Product(
        name="chicken",
        price=Decimal(5),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    chicken.save()
    queijo = Product(
        name="queijo",
        price=Decimal(2),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    queijo.save()
    bacon = Product(
        name="bacon",
        price=Decimal(3),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    bacon.save()
    chester = Product(
        name="chester",
        price=Decimal(6),
        category=adicional_id,
        is_active=True,
        currency=1,
    )
    chester.save()
    big_comps = [
        ProductComponent(product=big.id, component=hambuguer.id),
        ProductComponent(product=big.id, component=queijo.id),
    ]
    for big_comp in big_comps:
        big_comp.save()
    big_comps = [big_comp.id for big_comp in big_comps]

    cocorico_comps = [
        ProductComponent(product=cocorico.id, component=chicken.id),
        ProductComponent(product=cocorico.id, component=bacon.id),
    ]
    for cocorico_comp in cocorico_comps:
        cocorico_comp.save()
    cocorico_comps = [cocorico_comp.id for cocorico_comp in cocorico_comps]

    chester_b_comps = [
        ProductComponent(product=chester_b.id, component=chester.id),
    ]
    for chester_b_comp in chester_b_comps:
        chester_b_comp.save()
    chester_b_comps = [chester_b_comp.id for chester_b_comp in chester_b_comps]

    return [
        big.id,
        chester_b.id,
        cocorico.id,
        fritas.id,
        nuggets.id,
        doll.id,
        sukinho.id,
    ], [big_comps, cocorico_comps, chester_b_comps]


def _seed_purchases_selected_products_selected_products_components_and_payments(
    product_ids: List[int],
    components: List[List[int]],
    currency: int,
):
    # 1st purchase
    first_products = [
        SelectedProduct(product=product_ids[0]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in first_products:
        product.save()
    component = SelectedProductComponent(
        selected_product=first_products[0].id, component=components[0][0]
    )
    component.save()
    total_value = sum([product.product.price for product in first_products])
    first_purchase = 1
    purchase_selected_products = []
    for product in first_products:
        product.save()
        purchase_selected_products.append(
            PurchaseSelectedProducts(product=product.id, purchase_id=first_purchase)
        )
        purchase_selected_products[-1].save()

    # 2nd purchase
    second_products = [
        SelectedProduct(product=product_ids[1]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in second_products:
        product.save()
    total_value = sum([product.product.price for product in second_products])
    second_purchase = 2
    purchase_selected_products = []
    for product in second_products:
        product.save()
        purchase_selected_products.append(
            PurchaseSelectedProducts(product=product.id, purchase_id=second_purchase)
        )
        purchase_selected_products[-1].save()
    # 3th purchase
    third_products = [
        SelectedProduct(product=product_ids[1]),
        SelectedProduct(product=product_ids[2]),
        SelectedProduct(product=product_ids[0]),
    ]
    for product in third_products:
        product.save()
    total_value = sum([product.product.price for product in third_products])
    third_purchase = 3
    purchase_selected_products = []
    for product in third_products:
        product.save()
        purchase_selected_products.append(
            PurchaseSelectedProducts(product=product.id, purchase_id=third_purchase)
        )
        purchase_selected_products[-1].save()
    return [
        first_purchase,
        second_purchase,
        third_purchase,
    ]


def seed_data():
    bebidas, lanches, acompanhamentos, adicionais = _seed_category()
    currency = _seed_currency()
    product_ids, components = _seed_product_and_product_components(
        bebidas, lanches, acompanhamentos, adicionais
    )
    _seed_purchases_selected_products_selected_products_components_and_payments(
        product_ids, components, currency
    )
