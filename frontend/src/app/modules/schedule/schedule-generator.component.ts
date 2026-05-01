import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-schedule-generator',
  template: `
    <div class="container">
      <div class="card">
        <div class="card-header">
          <span>⚙️</span> Generate New Schedule
        </div>

        <div *ngIf="successMessage" class="alert alert-success">
          {{ successMessage }}
        </div>
        <div *ngIf="errorMessage" class="alert alert-error">
          {{ errorMessage }}
        </div>

        <form (ngSubmit)="generate()">
          <div class="grid grid-2" style="margin-top: 1.5rem;">
            <div class="form-group">
              <label>📅 Start Date</label>
              <input type="date" class="form-control" [(ngModel)]="startDate" name="startDate" required>
            </div>
            <div class="form-group">
              <label>📅 End Date</label>
              <input type="date" class="form-control" [(ngModel)]="endDate" name="endDate" required>
            </div>
          </div>

          <div class="form-group" style="margin-top: 1rem;">
            <label>👥 Select Staff (leave empty for all)</label>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap; margin-top: 0.5rem;">
              <label *ngFor="let staff of staffList" style="display: flex; align-items: center; gap: 0.5rem; cursor: pointer;">
                <input type="checkbox" [checked]="selectedStaff.includes(staff.id)" (change)="toggleStaff(staff.id)">
                {{ staff.name }} ({{ staff.role }})
              </label>
            </div>
          </div>

          <div style="margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; display: flex; gap: 1rem; align-items: center;">
            <button type="submit" class="btn btn-primary" [disabled]="loading" style="font-size: 1rem; padding: 0.75rem 2rem;">
              {{ loading ? '⏳ Generating...' : '🚀 Generate Schedule' }}
            </button>
            <div *ngIf="loading" style="color: #64748b;">
              This may take a few moments...
            </div>
          </div>
        </form>

        <!-- Generated Schedule Preview -->
        <div *ngIf="generatedSchedule" class="card" style="margin-top: 2rem; background: #f0fdf4; border: 1px solid #86efac;">
          <h3 style="color: #166534;">✅ Schedule Generated Successfully!</h3>
          <p><strong>Schedule:</strong> {{ generatedSchedule.schedule?.name }}</p>
          <p><strong>Entries:</strong> {{ generatedSchedule.entries?.length || 0 }} shifts assigned</p>
          <button class="btn btn-success" (click)="viewSchedule(generatedSchedule.schedule?.id)" style="margin-top: 1rem;">
            👁 View Schedule
          </button>
        </div>
      </div>

      <!-- Info Card -->
      <div class="card" style="background: #eff6ff; border: 1px solid #bfdbfe;">
        <h3 style="color: #1e40af;">📋 Scheduling Rules Applied</h3>
        <ul style="margin-top: 1rem; padding-left: 1.5rem; color: #1e3a8a;">
          <li>Night shifts assigned first with fairness constraints (min 8, max 10 per staff)</li>
          <li>Weekend coverage: 1 Morning + 1 Evening + 2 Night staff</li>
          <li>Weekday coverage: 1 Morning + 1 Evening + 1 Night staff</li>
          <li>Rest periods enforced after night shifts</li>
          <li>2 consecutive nights = 2 mandatory OFF days</li>
        </ul>
      </div>
    </div>
  `,
  imports: [CommonModule, FormsModule]
})
export class ScheduleGeneratorComponent implements OnInit {
  startDate: string = '';
  endDate: string = '';
  staffList: any[] = [];
  selectedStaff: number[] = [];
  loading = false;
  successMessage = '';
  errorMessage = '';
  generatedSchedule: any = null;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadStaff();
    // Set default dates (current month)
    const now = new Date();
    this.startDate = new Date(now.getFullYear(), now.getMonth(), 1).toISOString().split('T')[0];
    this.endDate = new Date(now.getFullYear(), now.getMonth() + 1, 0).toISOString().split('T')[0];
  }

  loadStaff() {
    this.http.get<any[]>('http://localhost:8000/api/v1/staff').subscribe({
      next: (data) => this.staffList = data,
      error: (err) => console.error('Error loading staff:', err)
    });
  }

  toggleStaff(staffId: number) {
    const index = this.selectedStaff.indexOf(staffId);
    if (index > -1) {
      this.selectedStaff.splice(index, 1);
    } else {
      this.selectedStaff.push(staffId);
    }
  }

  generate() {
    if (!this.startDate || !this.endDate) {
      this.errorMessage = 'Please select both start and end dates';
      return;
    }

    this.loading = true;
    this.errorMessage = '';
    this.successMessage = '';
    this.generatedSchedule = null;

    const payload: any = {
      start_date: this.startDate,
      end_date: this.endDate
    };

    if (this.selectedStaff.length > 0) {
      payload.staff_ids = this.selectedStaff;
    }

    this.http.post('http://localhost:8000/api/v1/schedules/generate', payload).subscribe({
      next: (response) => {
        this.generatedSchedule = response;
        this.successMessage = 'Schedule generated successfully!';
        this.loading = false;
      },
      error: (err) => {
        this.errorMessage = 'Error generating schedule: ' + (err.error?.detail || err.message);
        this.loading = false;
      }
    });
  }

  viewSchedule(scheduleId: number) {
    // Navigate to schedule view - you can implement routing later
    window.open(`http://localhost:4200/schedule/view/${scheduleId}`, '_blank');
  }
}
