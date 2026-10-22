from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models, transaction

from apps.inventory.models import Inventario
from apps.product.models import Product


class VentaQuerySet(models.QuerySet):
    def register(self, *, cliente, sucursal, fecha, items, impuestos=Decimal("0.00")):
        if not items:
            raise ValidationError({"items": ["La venta requiere al menos un producto."]})
        impuestos = Decimal(impuestos).quantize(Decimal("0.01"))
        if impuestos < 0:
            raise ValidationError({"impuestos": ["Los impuestos no pueden ser negativos."]})

        cantidades = {}
        for item in items:
            cantidad = int(item["cantidad"])
            if cantidad < 1:
                raise ValidationError({"items": ["La cantidad debe ser al menos 1."]})
            cantidades[item["producto_id"]] = cantidades.get(item["producto_id"], 0) + cantidad

        with transaction.atomic():
            if not cliente.is_active:
                raise ValidationError({"clienteId": ["El cliente no está activo."]})
            if not sucursal.is_active:
                raise ValidationError({"sucursalId": ["La sucursal no está activa."]})

            productos = Product.objects.in_bulk(list(cantidades))
            inventarios = {
                inv.producto_id: inv
                for inv in Inventario.objects.select_for_update()
                .filter(sucursal=sucursal, producto_id__in=cantidades)
                .order_by("producto_id")
            }

            for producto_id, cantidad in cantidades.items():
                producto = productos.get(producto_id)
                if producto is None:
                    raise ValidationError({"items": ["Hay productos que no existen."]})
                if not producto.is_active:
                    raise ValidationError({"items": [f"El producto {producto.nombre} no está activo."]})
                inventario = inventarios.get(producto_id)
                if inventario is None or inventario.cantidad < cantidad:
                    raise ValidationError({"items": [f"Stock insuficiente para {producto.nombre}."]})

            venta = self.model(
                cliente=cliente,
                sucursal=sucursal,
                fecha=fecha,
                impuestos=impuestos,
                estado=self.model.Estado.ACTIVA,
            )
            venta.save()

            for item in items:
                producto = productos[item["producto_id"]]
                venta.detalles.create(
                    producto=producto,
                    cantidad=int(item["cantidad"]),
                    valor_unitario=producto.precio,
                    observaciones=item.get("observaciones", ""),
                )

            subtotal = sum((detalle.total for detalle in venta.detalles.all()), Decimal("0.00"))
            venta.subtotal = subtotal.quantize(Decimal("0.01"))
            venta.total = (venta.subtotal + impuestos).quantize(Decimal("0.01"))
            venta.save(update_fields=["subtotal", "total", "updated_at"])

            for producto_id, cantidad in cantidades.items():
                inventario = inventarios[producto_id]
                inventario.cantidad -= cantidad
                inventario.save(update_fields=["cantidad", "updated_at"])

            return venta


class VentaManager(models.Manager.from_queryset(VentaQuerySet)):
    pass
