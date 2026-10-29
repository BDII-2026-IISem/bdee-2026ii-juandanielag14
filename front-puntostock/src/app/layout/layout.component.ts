import { Component } from '@angular/core';
import { RouterOutlet, RouterLink } from '@angular/router';

@Component({
  selector: 'app-layout',
  imports: [RouterOutlet, RouterLink],
  template: `
    <div class="min-h-screen flex flex-col bg-surface-50 dark:bg-surface-900">
      <!-- Header -->
      <header class="h-16 bg-primary text-primary-contrast flex items-center px-6 shadow-md">
        <h1 class="text-xl font-bold">PuntoStock</h1>
      </header>

      <div class="flex flex-1 overflow-hidden">
        <!-- Aside -->
        <aside class="w-64 bg-surface-0 dark:bg-surface-800 border-r border-surface-200 hidden md:flex flex-col p-4 gap-2">
          <a routerLink="/clientes" class="p-2 hover:bg-surface-100 rounded cursor-pointer">Clientes</a>
          <a routerLink="/productos" class="p-2 hover:bg-surface-100 rounded cursor-pointer">Productos</a>
          <a routerLink="/ventas" class="p-2 hover:bg-surface-100 rounded cursor-pointer">Ventas</a>
        </aside>

        <!-- Main Content -->
        <main class="flex-1 overflow-y-auto p-6">
          <router-outlet />
        </main>
      </div>

      <!-- Footer -->
      <footer class="h-12 bg-surface-100 dark:bg-surface-800 border-t border-surface-200 flex items-center justify-center text-sm text-surface-500">
        &copy; 2026 PuntoStock ERP
      </footer>
    </div>
  `
})
export class LayoutComponent {}
