import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-navbar',
  template: `
    <nav class="navbar">
      <a routerLink="/staff">Staff</a>
      <a routerLink="/schedule">Schedule</a>
    </nav>
  `,
  imports: [RouterLink]
})
export class NavbarComponent {}
