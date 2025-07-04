from copy import deepcopy
from datetime import datetime
from typing import List, Optional
from unittest.mock import MagicMock
import pytest

from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.domain.entities.categoria_entity import CategoriaEntity
from src.core.domain.entities.currency_entity import CurrencyEntity
from src.core.domain.entities.produto_escolhido_entity import (
    PartialProdutoEscolhidoEntity,
)
from src.core.domain.value_objects.preco_value_object import PrecoValueObject

from src.core.application.services.produto_service_command import ProductServiceCommand
from src.core.helpers.exceptions.incorrect_product_error import IncorrectProductError
from src.core.helpers.exceptions.item_not_found_error import ItemNotFoundError
from src.core.helpers.options.add_purchase_options import AddPurchaseOptions


class TestProductServiceCommand:
    @pytest.fixture
    def product_query(self):
        return MagicMock()

    @pytest.fixture
    def product_repository(self):
        return MagicMock()

    @pytest.fixture
    def currency_query(self):
        return MagicMock()

    @pytest.fixture
    def category_query(self):
        return MagicMock()

    @pytest.fixture
    def product_service(
        self,
        product_repository,
        product_query,
        category_query,
        currency_query,
    ):
        return ProductServiceCommand(
            product_repository=product_repository,
            product_query=product_query,
            currency_query=category_query,
            category_query=currency_query,
        )

    @pytest.fixture
    def preco(self):
        return PrecoValueObject(
            value=10,
            currency=CurrencyEntity(
                id=1,
                symbol="R$",
                name="Real",
                code="BRL",
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
        )

    @pytest.fixture
    def produto_entity(self, preco):
        return ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=preco,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=False,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
            allow_components=False,
        )

    def test_create_product_succesfully_pass_is_active_correctly(
        self, product_service: ProductServiceCommand, preco: PrecoValueObject
    ):
        product = PartialProdutoEntity(
            name="produto",
            description="produto_test_mock",
            price=preco,
            is_active=False,
        )
        expected_result = "mocked_product_aggregate"
        product_service.product_repository.create = MagicMock(
            return_value=expected_result
        )
        product_service.product_query.find = MagicMock(return_value=[])

        result = product_service.create_product(product)
        product_service.product_query.find.assert_called_once()
        product_service.product_repository.create.assert_called_once()
        assert result == expected_result

    def test_create_product_succesfully_pass_is_active_incorrectly(
        self, product_service: ProductServiceCommand, preco: PrecoValueObject
    ):
        product = PartialProdutoEntity(
            name="produto",
            description="produto_test_mock",
            price=preco,
            is_active=True,
        )
        expected_result = "mocked_product_aggregate"
        product_service.product_repository.create = MagicMock(
            return_value=expected_result
        )
        product_service.product_query.find = MagicMock(return_value=[])

        result = product_service.create_product(product)
        product_service.product_query.find.assert_called_once()
        product_service.product_repository.create.assert_called_once()
        assert result == expected_result

    def test_create_product_block_for_existing_produtc_with_same_name(
        self, product_service: ProductServiceCommand, preco: PrecoValueObject
    ):
        product = PartialProdutoEntity(
            name="produto",
            description="produto_test_mock",
            price=preco,
            is_active=False,
        )
        product_service.product_query.find = MagicMock(return_value=[product])

        with pytest.raises(ValueError, match="Já existe um produto com esse nome"):
            product_service.create_product(product)
        product_service.product_query.find.assert_called_once()
        product_service.product_repository.create.assert_not_called()

    def test_activate_product_successfully(
        self,
        product_service: ProductServiceCommand,
        preco: PrecoValueObject,
    ):
        product = ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=preco,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=False,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
            allow_components=True,
        )
        expected_result = "mocked_product_aggregate"
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=product)
        )
        product_service.product_repository.update = MagicMock(
            return_value=expected_result
        )
        result = product_service.activate_product(product.id)
        assert result == expected_result
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once_with(product)
        assert product.is_active is True

    def test_activate_product_blocked_because_no_product_found(
        self,
        product_service: ProductServiceCommand,
    ):
        product_service.product_query.get = MagicMock(return_value=None)
        product_service.product_repository.update = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto não encontrado"):
            product_service.activate_product(1)
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_activate_product_blocked_because_already_active(
        self,
        product_service: ProductServiceCommand,
        preco: PrecoValueObject,
    ):
        product = ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=preco,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=True,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=product)
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto já está ativo"):
            product_service.activate_product(1)
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_activate_product_blocked_because_no_category(
        self,
        product_service: ProductServiceCommand,
        preco: PrecoValueObject,
    ):
        product = ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=preco,
            category=None,
            is_active=False,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=product)
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto não possui categoria"):
            product_service.activate_product(1)
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_activate_product_blocked_because_no_price(
        self,
        product_service: ProductServiceCommand,
    ):
        product = ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=None,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=False,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=product)
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto não possui preço"):
            product_service.activate_product(1)
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_deactivate_product_successfully(
        self,
        product_service: ProductServiceCommand,
    ):
        product = ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=None,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=True,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        )
        expect_result = "mocked_product_aggregate"
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=product)
        )
        product_service.product_repository.update = MagicMock(
            return_value=expect_result
        )
        result = product_service.deactivate_product(1)
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once_with(product)
        assert result == expect_result
        assert product.is_active is False

    def test_deactivate_product_block_because_already_inactive(
        self,
        product_service: ProductServiceCommand,
    ):
        product = ProdutoEntity(
            id=1,
            name="produto",
            description="produto_test_mock",
            price=None,
            category=CategoriaEntity(
                name="categoria",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
            is_active=False,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
            components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=product)
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto já está inativo"):
            product_service.deactivate_product(1)
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()
        assert product.is_active is False

    def test_delete_product_successfully(
        self,
        product_service: ProductServiceCommand,
    ):
        product = ProdutoAggregate(
            product=ProdutoEntity(
                id=1,
                name="produto",
                description="produto_test_mock",
                price=None,
                category=CategoriaEntity(
                    name="categoria",
                    id=1,
                    created_at=datetime(2021, 1, 1),
                    updated_at=datetime(2021, 1, 1),
                ),
                is_active=False,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
                components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
            ),
            orders=[],
        )
        product_service.product_repository.get_by_product_id = MagicMock(
            return_value=product
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        product_service.delete_product(1)
        product_service.product_repository.get_by_product_id.assert_called_once()
        product_service.product_repository.delete.assert_called_once()

    def test_delete_product_fail_because_of_associated_orders(
        self,
        product_service: ProductServiceCommand,
    ):
        product = ProdutoAggregate(
            product=ProdutoEntity(
                id=1,
                name="produto",
                description="produto_test_mock",
                price=None,
                category=CategoriaEntity(
                    name="categoria",
                    id=1,
                    created_at=datetime(2021, 1, 1),
                    updated_at=datetime(2021, 1, 1),
                ),
                is_active=False,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
                components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
            ),
            orders=[1],
        )
        product_service.product_repository.get_by_product_id = MagicMock(
            return_value=product
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        with pytest.raises(
            ValueError, match="Produto possui pedidos associados, impossível deletar!"
        ):
            product_service.delete_product(1)
            product_service.product_repository.get_by_product_id.assert_called_once()
            product_service.product_repository.delete.assert_not_called()

    def test_delete_product_fail_because_product_is_active(
        self,
        product_service: ProductServiceCommand,
    ):
        product = ProdutoAggregate(
            product=ProdutoEntity(
                id=1,
                name="produto",
                description="produto_test_mock",
                price=None,
                category=CategoriaEntity(
                    name="categoria",
                    id=1,
                    created_at=datetime(2021, 1, 1),
                    updated_at=datetime(2021, 1, 1),
                ),
                is_active=True,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
                components=[PartialProdutoEntity(id=2), PartialProdutoEntity(id=3)],
            ),
            orders=[],
        )
        product_service.product_repository.get_by_product_id = MagicMock(
            return_value=product
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto ativo, impossível deletar!"):
            product_service.delete_product(1)
            product_service.product_repository.get_by_product_id.assert_called_once()
            product_service.product_repository.delete.assert_not_called()

    def test_delete_product_fail_because_product_not_found(
        self,
        product_service: ProductServiceCommand,
    ):
        product_service.product_repository.get_by_product_id = MagicMock(
            return_value=None
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        with pytest.raises(ValueError, match="Produto não encontrado"):
            product_service.delete_product(1)
            product_service.product_repository.get_by_product_id.assert_called_once()
            product_service.product_repository.delete.assert_not_called()

    def test_update_product_successfully_change_name(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.name = "produto_novo"
        input_product.allow_components = True
        product_service.product_repository.update = MagicMock(return_value=None)
        product_service.product_query.find = MagicMock(return_value=[])
        # act
        product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once()

    def test_update_product_successfully_change_category(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.category = CategoriaEntity(
            name="categoria_nova",
            id=1,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        input_product.allow_components = True
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once()

    def test_update_product_successfully_change_price(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.price = PrecoValueObject(
            value=12,
            currency=CurrencyEntity(
                symbol="R$",
                name="Real",
                code="BRL",
                id=1,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
        )
        input_product.allow_components = True
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once()

    def test_update_product_succefully_change_allow_components_to_false(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.allow_components = False
        input_product.components = []
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once()

    def test_update_product_succefully_change_allow_components_to_true(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.allow_components = True
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_called_once()

    def test_update_product_fail_because_product_not_found(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(return_value=None)
        input_product = deepcopy(produto)
        input_product.name = "produto_novo"
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        with pytest.raises(ValueError, match="Produto não encontrado"):
            product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_name_already_exists(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        input_product = deepcopy(produto)
        input_product.name = "produto_novo"
        product_service.product_repository.update = MagicMock(return_value=None)
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )

        # act
        with pytest.raises(ValueError, match="Já existe um produto com esse nome"):
            product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_category_does_not_exists(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        input_product = deepcopy(produto)
        input_product.category = CategoriaEntity(
            name="categoria_nova",
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        product_service.category_query.get = MagicMock(return_value=None)
        # act
        with pytest.raises(ValueError, match="Categoria não encontrada"):
            product_service.update_product(input_product)

        # assert
        product_service.product_query.get.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_price_is_invalid(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        input_product = deepcopy(produto)
        input_product.price = input_product.price = PrecoValueObject(
            value=-12,
            currency=CurrencyEntity(
                symbol="R$",
                name="Real",
                code="BRL",
                id=2,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )

        # act
        with pytest.raises(ValueError, match="Preço não pode ser negativo"):
            product_service.update_product(input_product)

        input_product.price = input_product.price = PrecoValueObject(
            value=0,
            currency=CurrencyEntity(
                symbol="R$",
                name="Real",
                code="BRL",
                id=2,
                created_at=datetime(2021, 1, 1),
                updated_at=datetime(2021, 1, 1),
            ),
        )
        with pytest.raises(ValueError, match="Preço não pode ser zero"):
            product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_category_is_component_and_is_trying_to_allow_and_or_add_components(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.allow_components = True
        input_product.category = CategoriaEntity(
            name="acompanhamento",
            is_component=True,
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        with pytest.raises(
            ValueError, match="Um Acompanhamento não permite ter outros acompanhamentos"
        ):
            product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_does_not_allow_components_and_is_trying_add_components(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto)
        )
        input_product = deepcopy(produto)
        input_product.allow_components = False
        input_product.category = CategoriaEntity(
            name="acompanhamento",
            is_component=True,
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        input_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
        ]
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        with pytest.raises(
            ValueError,
            match="Produto não permite acompanhamentos, mas possui acompanhamentos",
        ):
            product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_category_is_adding_product_as_component_but_isnt_tagged_as_component(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        component_mock = deepcopy(produto)
        component_mock.category = CategoriaEntity(
            is_component=False,
            name="not_acompanhamento_mock",
            id=4,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto),
        )
        product_service.product_query.get_only_entity = MagicMock(
            return_value=component_mock
        )
        input_product = deepcopy(produto)
        input_product.allow_components = True
        input_product.category = CategoriaEntity(
            name="produto_principal",
            is_component=False,
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        input_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
            PartialProdutoEntity(id=4),
        ]
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        with pytest.raises(
            ValueError,
            match="Apenas produtos do tipo 'Acompanhamento' podem ser acompanhamentos",
        ):
            product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_trying_to_add_itself_as_component(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        input_product = deepcopy(produto)
        input_product.allow_components = True
        input_product.category = CategoriaEntity(
            name="produto_principal",
            is_component=False,
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        input_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=1),
        ]
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto),
        )
        product_service.product_query.get_only_entity = MagicMock(return_value=produto)
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        with pytest.raises(
            ValueError,
            match="Um produto não pode ser componente de si mesmo",
        ):
            product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_not_called()

    def test_update_product_fail_because_category_is_adding_the_same_product_as_component_twice(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        component_mock = deepcopy(produto)
        component_mock.id = 2
        component_mock.category = CategoriaEntity(
            is_component=True,
            name="acompanhamento_mock",
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto),
        )
        product_service.product_query.get_only_entity = MagicMock(
            return_value=component_mock
        )
        input_product = deepcopy(produto)
        input_product.allow_components = True
        input_product.category = CategoriaEntity(
            name="produto_principal",
            is_component=False,
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        input_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=2),
        ]
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        with pytest.raises(
            ValueError,
            match="Acompanhamentos não podem ser duplicados",
        ):
            product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_not_called()

    def test_update_product_successfully_adding_a_new_component(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        produto = produto_entity
        component_mock = deepcopy(produto)
        component_mock.id = 3
        component_mock.category = CategoriaEntity(
            is_component=True,
            name="acompanhamento_mock",
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        product_service.product_query.get = MagicMock(
            return_value=ProdutoAggregate(product=produto),
        )
        product_service.product_query.get_only_entity = MagicMock(
            return_value=component_mock
        )
        input_product = deepcopy(produto)
        input_product.allow_components = True
        input_product.category = CategoriaEntity(
            name="produto_principal",
            is_component=False,
            id=2,
            created_at=datetime(2021, 1, 1),
            updated_at=datetime(2021, 1, 1),
        )
        input_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
        ]
        product_service.product_repository.update = MagicMock(return_value=None)

        # act
        product_service.update_product(input_product)

        # assert
        product_service.product_repository.update.assert_called()

    def test_get_all_by_purchase_has_products(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        product = deepcopy(produto_entity)
        product.id = 1
        product_service.product_query.get_by_purchase_id = MagicMock(
            return_value=[ProdutoAggregate(product=product)]
        )

        # act
        result = product_service.get_all_by_purchase(1)

        # assert
        assert len(result) == 1
        assert result[0].product.id == 1

    def test_get_all_by_purchase_does_not_has_products(
        self, product_service: ProductServiceCommand
    ):
        # arrange
        product_service.product_query.get_by_purchase_id = MagicMock(return_value=[])

        # act
        result = product_service.get_all_by_purchase(1)

        # assert
        assert len(result) == 0

    def test_add_purchase_fail_because_product_not_found(
        self, product_service: ProductServiceCommand
    ):
        # arrange
        product_service.product_query.get_all_ids = MagicMock(return_value=[])
        product_service.product_repository.update = MagicMock(return_value=None)
        options = [AddPurchaseOptions(product_id=1), AddPurchaseOptions(product_id=2)]
        # act
        with pytest.raises(
            ItemNotFoundError,
            match="Um ou mais produtos não encontrados, missing IDs: 1, 2",
        ):
            product_service.add_purchase(1, options)

        # assert
        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_add_purchase_fail_because_component_does_not_exists(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        product_service.product_query.get_all_ids = MagicMock(
            return_value=[ProdutoAggregate(product=produto_entity)]
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        options = [AddPurchaseOptions(product_id=1, components=[2, 3])]
        # act
        with pytest.raises(
            ItemNotFoundError,
            match="Um ou mais produtos não encontrados, missing IDs: 2, 3",
        ):
            product_service.add_purchase(1, options)

        # assert
        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_add_purchase_fail_because_product_does_not_allow_components(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = False
        component_product = deepcopy(produto_entity)
        component_product.id = 2

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
            ]
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        options = [AddPurchaseOptions(product_id=1, components=[2])]
        # act
        with pytest.raises(
            IncorrectProductError,
            match="Acompanhamento selecionado, mas produto não permite acompanhamentos",
        ):
            product_service.add_purchase(1, options)

        # assert
        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_add_purchase_fail_because_product_does_not_have_components(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = []
        component_product = deepcopy(produto_entity)
        component_product.id = 2

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
            ]
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        options = [AddPurchaseOptions(product_id=1, components=[2])]
        # act
        with pytest.raises(
            IncorrectProductError,
            match="Acompanhamento selecionado, mas produto não possui acompanhamentos",
        ):
            product_service.add_purchase(1, options)

        # assert
        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_add_purchase_fail_because_product_does_not_have_specified_component(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = [PartialProdutoEntity(id=3)]
        component_product = deepcopy(produto_entity)
        component_product.id = 2

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
            ]
        )
        product_service.product_repository.update = MagicMock(return_value=None)
        options = [AddPurchaseOptions(product_id=1, components=[2])]
        # act
        with pytest.raises(
            IncorrectProductError,
            match="Acompanhamento não encontrado ou não permitido para este produto",
        ):
            product_service.add_purchase(1, options)

        # assert
        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.update.assert_not_called()

    def test_add_purchase_success_clean_purchase(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = [PartialProdutoEntity(id=2)]
        component_product = deepcopy(produto_entity)
        component_product.id = 2
        set_product = ProdutoAggregate(product=main_product, orders=[1])

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
            ]
        )
        product_service.product_query.get_by_purchase_id = MagicMock(return_value=None)
        product_service.product_repository.delete = MagicMock(return_value=None)
        product_service.product_repository.set_selected_product_and_components = (
            MagicMock(return_value=set_product)
        )

        options = [AddPurchaseOptions(product_id=1, components=[2])]
        # act

        result = product_service.add_purchase(1, options)

        # assert
        assert len(result) == 1
        assert result[0] == set_product

        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.delete.assert_not_called()
        product_service.product_repository.set_selected_product_and_components.assert_called_once()

    def test_add_purchase_success_change_component_from_product(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
        ]
        component_product = deepcopy(produto_entity)
        component_product.id = 2
        set_product = ProdutoAggregate(product=main_product, orders=[1])

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
            ]
        )
        product_service.product_query.get_by_purchase_id = MagicMock(
            return_value=[ProdutoAggregate(product=main_product)]
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        product_service.product_repository.set_selected_product_and_components = (
            MagicMock(return_value=set_product)
        )

        options = [AddPurchaseOptions(product_id=1, components=[2])]
        # act

        result = product_service.add_purchase(1, options)

        # assert
        assert len(result) == 1
        assert result[0] == set_product

        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.delete.assert_called_once()
        product_service.product_repository.set_selected_product_and_components.assert_called_once()

    def test_add_purchase_success_add_component_to_product(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
        ]
        component_product = deepcopy(produto_entity)
        component_product.id = 2
        second_component_product = deepcopy(produto_entity)
        second_component_product.id = 3
        set_product = ProdutoAggregate(product=main_product, orders=[1])

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
                ProdutoAggregate(product=second_component_product),
            ]
        )
        product_service.product_query.get_by_purchase_id = MagicMock(
            return_value=[ProdutoAggregate(product=main_product)]
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        product_service.product_repository.set_selected_product_and_components = (
            MagicMock(return_value=set_product)
        )

        options = [AddPurchaseOptions(product_id=1, components=[2, 3])]
        # act

        result = product_service.add_purchase(1, options)

        # assert
        assert len(result) == 1
        assert result[0] == set_product

        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.delete.assert_called_once()
        product_service.product_repository.set_selected_product_and_components.assert_called_once()

    def test_add_purchase_success_remove_component_from_product(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
        ]
        component_product = deepcopy(produto_entity)
        component_product.id = 2

        set_product = ProdutoAggregate(product=main_product, orders=[1])

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=main_product),
                ProdutoAggregate(product=component_product),
            ]
        )
        product_service.product_query.get_by_purchase_id = MagicMock(
            return_value=[ProdutoAggregate(product=main_product)]
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        product_service.product_repository.set_selected_product_and_components = (
            MagicMock(return_value=set_product)
        )

        options = [AddPurchaseOptions(product_id=1, components=[2])]
        # act

        result = product_service.add_purchase(1, options)

        # assert
        assert len(result) == 1
        assert result[0] == set_product

        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.delete.assert_called_once()
        product_service.product_repository.set_selected_product_and_components.assert_called_once()

    def test_add_purchase_success_remove_product_from_purchase(
        self, product_service: ProductServiceCommand, produto_entity: ProdutoEntity
    ):
        # arrange
        main_product = deepcopy(produto_entity)
        main_product.allow_components = True
        main_product.components = [
            PartialProdutoEntity(id=2),
            PartialProdutoEntity(id=3),
        ]
        secondary_product = deepcopy(produto_entity)
        secondary_product.id = 4
        component_product = deepcopy(produto_entity)
        component_product.id = 2

        set_product = ProdutoAggregate(product=secondary_product, orders=[1])

        product_service.product_query.get_all_ids = MagicMock(
            return_value=[
                ProdutoAggregate(product=secondary_product),
            ]
        )
        product_service.product_query.get_by_purchase_id = MagicMock(
            return_value=[ProdutoAggregate(product=main_product)]
        )
        product_service.product_repository.delete = MagicMock(return_value=None)
        product_service.product_repository.set_selected_product_and_components = (
            MagicMock(return_value=set_product)
        )

        options = [AddPurchaseOptions(product_id=4)]
        # act

        result = product_service.add_purchase(1, options)

        # assert
        assert len(result) == 1
        assert result[0] == set_product

        product_service.product_query.get_all_ids.assert_called_once()
        product_service.product_repository.delete.assert_called_once()
        product_service.product_repository.set_selected_product_and_components.assert_called_once()
