import { Component, computed, effect, signal } from '@angular/core';
import { ButtonModule } from 'primeng/button';
import { CardModule } from 'primeng/card';

interface Producto {
  nombre: string;
  precio: number;
  activo: boolean;
}

@Component({
  host: { class: 'block' },
  selector: 'app-ejemplo',
  imports: [ButtonModule, CardModule],
  templateUrl: './ejemplo.html',
  styleUrl: './ejemplo.css',
})
export class Ejemplo {
  readonly producto = signal<Producto>({ nombre: 'Café molido 500 g', precio: 18000, activo: true });

  /** IVA del 19 % (Colombia), derivado del signal. */
  readonly precioConIva = computed(() => Math.round(this.producto().precio * 1.19));
  readonly estadoTexto = computed(() => (this.producto().activo ? 'Activo' : 'Inactivo'));

  constructor() {
    effect(() => console.info(`[ejemplo] ${this.producto().nombre} · ${this.producto().precio}`));
  }

  subirPrecio(): void {
    this.producto.update((p) => ({ ...p, precio: p.precio + 1000 }));
  }

  alternarEstado(): void {
    this.producto.update((p) => ({ ...p, activo: !p.activo }));
  }

  reiniciar(): void {
    this.producto.set({ nombre: 'Café molido 500 g', precio: 18000, activo: true });
  }
}
