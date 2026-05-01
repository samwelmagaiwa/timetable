import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { ApiService } from '../../core/api.service';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  template: `
    <div class="container">
      <h1 style="margin-bottom: 2rem; color: #1e293b;">📊 Dashboard</h1>

      <!-- Stats Cards -->
      <div class="grid grid-3" style="margin-bottom: 2rem;">
        <div class="card" style="text-align: center; background: linear-gradient(135deg, #dbeafe, #bfdbfe); border: none;">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">👥</div>
          <h2 style="font-size: 2rem; color: #1e40af; margin: 0;">{{ staffCount }}</h2>
          <p style="color: #3b82f6; margin-top: 0.5rem;">Active Staff</p>
        </div>

        <div class="card" style="text-align: center; background: linear-gradient(135deg, #d1fae5, #a7f3d2); border: none;">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📋</div>
          <h2 style="font-size: 2rem; color: #065f46; margin: 0;">{{ scheduleCount }}</h2>
          <p style="color: #10b981; margin-top: 0.5rem;">Schedules Created</p>
        </div>

        <div class="card" style="text-align: center; background: linear-gradient(135deg, #fef3c7, #fde68a); border: none;">
          <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🌙</div>
          <h2 style="font-size: 2rem; color: #92400e; margin: 0;">{{ nightShiftsThisMonth }}</h2>
          <p style="color: #f59e0b; margin-top: 0.5rem;">Night Shifts (This Month)</p>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="card">
        <div class="card-header">⚡ Quick Actions</div>
        <div class="grid grid-2" style="margin-top: 1rem;">
          <a routerLink="/schedule/generate" class="card" style="text-decoration: none; color: inherit; display: block; transition: transform 0.2s;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚙️</div>
            <h3 style="color: #2563eb;">Generate Schedule</h3>
            <p style="color: #64748b; font-size: 0.875rem;">Create a new automated schedule</p>
          </a>
          <a routerLink="/staff" class="card" style="text-decoration: none; color: inherit; display: block; transition: transform 0.2s;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">👥</div>
            <h3 style="color: #2563eb;">Manage Staff</h3>
            <p style="color: #64748b; font-size: 0.875rem;">Add or edit staff members</p>
          </a>
        </div>
      </div>

      <!-- Recent Schedules -->
      <div class="card" style="margin-top: 1.5rem;">
        <div class="card-header">📋 Recent Schedules</div>
        <div *ngIf="recentSchedules.length === 0" style="text-align: center; padding: 2rem; color: #64748b;">
          No schedules yet. <a routerLink="/schedule/generate" style="color: #2563eb;">Generate one now!</a>
        </div>
        <div *ngFor="let schedule of recentSchedules" class="card" style="background: #f8fafc; margin-top: 1rem;">
          <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
              <h4 style="margin: 0; color: #1e293b;">{{ schedule.name }}</h4>
              <p style="margin: 0.25rem 0 0 0; color: #64748b; font-size: 0.875rem;">
                {{ schedule.start_date }} to {{ schedule.end_date }}
              </p>
            </div>
            <span class="badge" [ngClass]="schedule.is_locked ? 'badge-night' : 'badge-morning'">
              {{ schedule.is_locked ? '🔒 Locked' : '🔓 Active' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  `,
  imports: [CommonModule, RouterLink]
})
export class DashboardComponent implements OnInit {
  staffCount = 0;
  scheduleCount = 0;
  nightShiftsThisMonth = 0;
  recentSchedules: any[] = [];

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.loadDashboardData();
  }

  loadDashboardData() {
    // Load staff count
    this.apiService.get<any[]>('/api/v1/staff').subscribe({
      next: (data) => this.staffCount = data.length,
      error: (err) => console.error('Error loading staff:', err)
    });

    // Load schedules
    const now = new Date();
    this.apiService.get<any[]>(`/api/v1/schedules/month/${now.getFullYear()}/${now.getMonth() + 1}`).subscribe({
      next: (data) => {
        this.scheduleCount = data.length;
        this.recentSchedules = data.slice(0, 5); // Show last 5
      },
      error: (err) => console.error('Error loading schedules:', err)
    });
  }
}
