import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ApiService } from '../../core/api.service';
import { forkJoin } from 'rxjs';

@Component({
  selector: 'app-schedule-view',
  standalone: true,
  template: `
    <div class="container">
      <div class="card">
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
          <span>📋 Schedule View</span>
          <div style="display: flex; gap: 0.5rem; align-items: center;">
            <button class="btn btn-secondary" (click)="prevMonth()">◀</button>
            <span style="font-weight: 600; min-width: 140px; text-align: center;">{{ currentMonth }}</span>
            <button class="btn btn-secondary" (click)="nextMonth()">▶</button>
          </div>
        </div>

        <!-- Legend -->
        <div style="display: flex; gap: 1.5rem; margin: 1rem 0; flex-wrap: wrap;">
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-morning">M</span> Morning
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-evening">E</span> Evening
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-night">N</span> Night
          </div>
          <div style="display: flex; align-items: center; gap: 0.5rem;">
            <span class="badge badge-off">—</span> Off / Rest
          </div>
        </div>

        <!-- Loading -->
        <div *ngIf="loading" style="text-align: center; padding: 3rem; color: #64748b;">
          ⏳ Loading schedule...
        </div>

        <!-- No Data -->
        <div *ngIf="!loading && scheduleGrid.length === 0" style="text-align: center; padding: 3rem; color: #94a3b8;">
          <p style="font-size: 1.25rem;">📅 No schedule found for this month.</p>
          <p style="margin-top: 0.5rem;">Go to <strong>Generate</strong> to create one.</p>
        </div>

        <!-- Calendar Grid -->
        <div *ngIf="!loading && scheduleGrid.length > 0" class="table-container">
          <table>
            <thead>
              <tr>
                <th style="min-width: 160px; position: sticky; left: 0; background: #f1f5f9; z-index: 1;">Staff</th>
                <th *ngFor="let day of days" style="text-align: center; min-width: 50px;" [style.background]="day.isWeekend ? '#fef3c7' : ''">
                  <div style="font-weight: 700;">{{ day.date }}</div>
                  <div style="font-size: 0.7rem; color: #94a3b8;">{{ day.dayShort }}</div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let row of scheduleGrid">
                <td style="font-weight: 600; white-space: nowrap; position: sticky; left: 0; background: white; z-index: 1;">{{ row.staffName }}</td>
                <td *ngFor="let shift of row.shifts" style="text-align: center; padding: 0.5rem 0.25rem;">
                  <span *ngIf="shift !== '—'" class="badge" [ngClass]="getBadgeClass(shift)">
                    {{ shift }}
                  </span>
                  <span *ngIf="shift === '—'" style="color: #cbd5e1;">—</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Stats -->
        <div *ngIf="!loading && stats && stats.totalShifts > 0" class="grid grid-3" style="margin-top: 1.5rem;">
          <div class="card" style="text-align: center; background: #dbeafe;">
            <h3 style="color: #1e40af;">{{ stats.totalShifts }}</h3>
            <p style="color: #3b82f6;">Total Shifts</p>
          </div>
          <div class="card" style="text-align: center; background: #d1fae5;">
            <h3 style="color: #065f46;">{{ stats.nightShifts }}</h3>
            <p style="color: #10b981;">Night Shifts</p>
          </div>
          <div class="card" style="text-align: center; background: #fef3c7;">
            <h3 style="color: #92400e;">{{ stats.morningShifts }}</h3>
            <p style="color: #f59e0b;">Morning Shifts</p>
          </div>
        </div>
      </div>
    </div>
  `,
  imports: [CommonModule]
})
export class ScheduleViewComponent implements OnInit {
  currentDate = new Date();
  currentMonth = '';
  days: any[] = [];
  scheduleGrid: any[] = [];
  loading = false;
  stats: any = null;
  staffMap: { [id: number]: string } = {};

  constructor(private apiService: ApiService) { }

  ngOnInit() {
    this.updateMonth();
    this.loadSchedule();
  }

  updateMonth() {
    this.currentMonth = this.currentDate.toLocaleString('default', { month: 'long', year: 'numeric' });
    this.generateDays();
  }

  generateDays() {
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth();
    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    this.days = [];
    for (let d = new Date(firstDay); d <= lastDay; d.setDate(d.getDate() + 1)) {
      const dow = d.getDay();
      this.days.push({
        date: d.getDate(),
        dayShort: d.toLocaleString('default', { weekday: 'short' }),
        fullDate: d.toISOString().split('T')[0],
        isWeekend: dow === 0 || dow === 6
      });
    }
  }

  prevMonth() {
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() - 1, 1);
    this.updateMonth();
    this.loadSchedule();
  }

  nextMonth() {
    this.currentDate = new Date(this.currentDate.getFullYear(), this.currentDate.getMonth() + 1, 1);
    this.updateMonth();
    this.loadSchedule();
  }

  loadSchedule() {
    this.loading = true;
    this.scheduleGrid = [];
    this.stats = null;
    const year = this.currentDate.getFullYear();
    const month = this.currentDate.getMonth() + 1;

    // Load both staff list and schedules for this month
    forkJoin({
      staff: this.apiService.get<any[]>('/api/v1/staff'),
      schedules: this.apiService.get<any[]>(`/api/v1/schedules/month/${year}/${month}`)
    }).subscribe({
      next: ({ staff, schedules }) => {
        // Build staff ID → name map
        this.staffMap = {};
        for (const s of staff) {
          this.staffMap[s.id] = s.name;
        }

        if (schedules.length === 0) {
          this.loading = false;
          return;
        }

        // Use the most recent schedule
        const schedule = schedules[schedules.length - 1];

        // Fetch entries for this schedule
        this.apiService.get<any[]>(`/api/v1/schedules/${schedule.id}/entries`).subscribe({
          next: (entries) => {
            this.processEntries(entries, staff);
            this.loading = false;
          },
          error: (err) => {
            console.error('Error loading entries:', err);
            this.loading = false;
          }
        });
      },
      error: (err) => {
        console.error('Error loading schedule data:', err);
        this.loading = false;
      }
    });
  }

  processEntries(entries: any[], staffList: any[]) {
    // Build a lookup: staffId → { date → shiftType }
    const shiftMap: { [staffId: number]: { [date: string]: string } } = {};
    const staffIds = new Set<number>();

    for (const entry of entries) {
      staffIds.add(entry.staff_id);
      if (!shiftMap[entry.staff_id]) {
        shiftMap[entry.staff_id] = {};
      }
      shiftMap[entry.staff_id][entry.date] = entry.shift_type;
    }

    // Build grid rows
    this.scheduleGrid = [];
    for (const staff of staffList) {
      if (!staffIds.has(staff.id)) continue; // Skip staff not in this schedule

      const shifts: string[] = [];
      for (const day of this.days) {
        const shiftType = shiftMap[staff.id]?.[day.fullDate] || '—';
        shifts.push(shiftType);
      }

      this.scheduleGrid.push({
        staffName: staff.name,
        staffId: staff.id,
        shifts
      });
    }

    // Compute stats
    let totalShifts = 0;
    let nightShifts = 0;
    let morningShifts = 0;

    for (const entry of entries) {
      totalShifts++;
      if (entry.shift_type === 'N') nightShifts++;
      if (entry.shift_type === 'M') morningShifts++;
    }

    this.stats = { totalShifts, nightShifts, morningShifts };
  }

  getBadgeClass(shift: string): string {
    switch (shift) {
      case 'M': return 'badge-morning';
      case 'E': return 'badge-evening';
      case 'N': return 'badge-night';
      default: return 'badge-off';
    }
  }
}
