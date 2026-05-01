import { Component } from '@angular/core';
import { RouterLink, RouterLinkActive } from '@angular/router';

@Component({
  selector: 'app-navbar',
  standalone: true,
  template: `
    <nav class="navbar">
      <div class="nav-brand">
        <span class="nav-logo">📅</span>
        <span class="nav-title">Timetable System</span>
      </div>
      <div class="nav-links">
        <a routerLink="/dashboard" routerLinkActive="active" class="nav-link">
          <span class="nav-icon">📊</span> Dashboard
        </a>
        <a routerLink="/staff" routerLinkActive="active" class="nav-link">
          <span class="nav-icon">👥</span> Staff
        </a>
        <a routerLink="/schedule" routerLinkActive="active" class="nav-link">
          <span class="nav-icon">📋</span> Schedule
        </a>
        <a routerLink="/schedule/generate" routerLinkActive="active" class="nav-link">
          <span class="nav-icon">⚙️</span> Generate
        </a>
      </div>
    </nav>
  `,
  styles: [`
    .navbar {
      background: linear-gradient(135deg, #2563eb, #1d4ed8);
      padding: 1rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      flex-wrap: wrap;
      gap: 0.75rem;
    }
    .nav-brand {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: white;
      font-weight: 600;
      font-size: 1.25rem;
    }
    .nav-logo {
      font-size: 1.5rem;
    }
    .nav-links {
      display: flex;
      gap: 0.5rem;
      flex-wrap: wrap;
    }
    .nav-link {
      color: white;
      text-decoration: none;
      padding: 0.5rem 1rem;
      border-radius: 8px;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      transition: background 0.2s;
      white-space: nowrap;
      font-size: 0.9rem;
    }
    .nav-link:hover, .nav-link.active {
      background: rgba(255,255,255,0.2);
    }
    .nav-icon {
      font-size: 1.125rem;
    }
    @media (max-width: 768px) {
      .navbar {
        padding: 0.75rem 1rem;
        justify-content: center;
      }
      .nav-links {
        gap: 0.25rem;
        justify-content: center;
      }
      .nav-link {
        padding: 0.375rem 0.75rem;
        font-size: 0.8rem;
      }
    }
    @media (max-width: 480px) {
      .navbar {
        flex-direction: column;
        gap: 0.5rem;
      }
      .nav-links {
        width: 100%;
        justify-content: center;
      }
    }
  `],
  imports: [RouterLink, RouterLinkActive]
})
export class NavbarComponent { }
