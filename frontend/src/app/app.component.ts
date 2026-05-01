import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/navbar/navbar.component';

@Component({
  selector: 'app-root',
  template: `
    <app-navbar></app-navbar>
    <main style="min-height: calc(100vh - 70px); background: #f1f5f9;">
      <div class="container" style="padding-top: 2rem; padding-bottom: 2rem;">
        <router-outlet></router-outlet>
      </div>
    </main>
    <footer style="background: #1e293b; color: white; text-align: center; padding: 1rem;">
      <p style="margin: 0; font-size: 0.875rem;">© 2026 Timetable System - Automated Staff Scheduling</p>
    </footer>
  `,
  imports: [RouterOutlet, NavbarComponent]
})
export class AppComponent {}
