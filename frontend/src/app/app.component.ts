import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { NavbarComponent } from './shared/navbar/navbar.component';

@Component({
  selector: 'app-root',
  standalone: true,
  template: `
    <app-navbar></app-navbar>
    <main style="min-height: calc(100vh - 70px); background: #f1f5f9;">
      <div style="width: 100%; max-width: 1600px; margin: 0 auto; padding: 1.5rem 2rem;">
        <router-outlet></router-outlet>
      </div>
    </main>
    <footer style="background: #1e293b; color: white; text-align: center; padding: 1rem;">
      <p style="margin: 0; font-size: 0.875rem;">© 2026 Timetable System - Automated Staff Scheduling</p>
    </footer>
  `,
  imports: [RouterOutlet, NavbarComponent]
})
export class AppComponent { }
