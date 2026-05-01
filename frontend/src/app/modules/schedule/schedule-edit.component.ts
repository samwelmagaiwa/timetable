import { Component, OnInit, Input } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-schedule-edit',
  template: `
    <div class="container">
      <div class="card">
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
          <span>✏️ Edit Schedule</span>
          <button class="btn btn-secondary" (click)="goBack()">← Back</button>
        </div>

        <div *ngIf="loading" style="text-align: center; padding: 3rem;">
          ⏳ Loading schedule entries...
        </div>

        <div *ngIf="!loading && entries.length > 0">
          <div class="table-container" style="margin-top: 1.5rem;">
            <table>
              <thead>
                <tr>
                  <th>Date</th>
                  <th>Staff</th>
                  <th>Shift Type</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr *ngFor="let entry of entries">
                  <td>
                    <strong>{{ entry.date }}</strong><br>
                    <small style="color: #64748b;">{{ getDayName(entry.date) }}</small>
                  </td>
                  <td>{{ getStaffName(entry.staff_id) }}</td>
                  <td>
                    <span class="badge" [ngClass]="getBadgeClass(entry.shift_type)">
                      {{ entry.shift_type }}
                    </span>
                  </td>
                  <td>
                    <select class="form-control" style="width: auto; display: inline-block;"
                            [value]="entry.shift_type"
                            (change)="updateShift(entry, $event)">
                      <option value="M">🌅 Morning</option>
                      <option value="E">🌆 Evening</option>
                      <option value="N">🌙 Night</option>
                      <option value="O">😴 Off</option>
                    </select>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <div style="margin-top: 1.5rem; padding: 1rem; background: #fef3c7; border-radius: 8px;">
            <p style="margin: 0; color: #92400e;">
              ⚠️ Changes are saved automatically. Make sure to follow scheduling rules.
            </p>
          </div>
        </div>

        <div *ngIf="!loading && entries.length === 0" style="text-align: center; padding: 3rem; color: #64748b;">
          No schedule entries found. <a routerLink="/schedule/generate" style="color: #2563eb;">Generate a schedule</a> first.
        </div>
      </div>
    </div>
  `,
  imports: [CommonModule, FormsModule]
})
export class ScheduleEditComponent implements OnInit {
  @Input() scheduleId?: number;
  entries: any[] = [];
  staffList: any[] = [];
  loading = true;

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadStaff();
    this.loadEntries();
  }

  loadStaff() {
    this.http.get<any[]>('http://localhost:8000/api/v1/staff').subscribe({
      next: (data) => this.staffList = data,
      error: (err) => console.error('Error loading staff:', err)
    });
  }

  loadEntries() {
    if (!this.scheduleId) return;
    
    this.http.get<any[]>(`http://localhost:8000/api/v1/schedules/${this.scheduleId}/entries`).subscribe({
      next: (data) => {
        this.entries = data;
        this.loading = false;
      },
      error: (err) => {
        console.error('Error loading entries:', err);
        this.loading = false;
      }
    });
  }

  getStaffName(staffId: number): string {
    const staff = this.staffList.find(s => s.id === staffId);
    return staff ? staff.name : 'Unknown';
  }

  getDayName(dateStr: string): string {
    const date = new Date(dateStr);
    return date.toLocaleString('default', { weekday: 'long' });
  }

  getBadgeClass(shiftType: string): string {
    switch(shiftType) {
      case 'M': return 'badge-morning';
      case 'E': return 'badge-evening';
      case 'N': return 'badge-night';
      default: return 'badge-off';
    }
  }

  updateShift(entry: any, event: any) {
    const newType = event.target.value;
    
    this.http.put(`http://localhost:8000/api/v1/schedules/shift/${entry.id}`, {
      shift_type: newType
    }).subscribe({
      next: () => {
        entry.shift_type = newType;
        console.log('Shift updated successfully');
      },
      error: (err) => {
        console.error('Error updating shift:', err);
        alert('Error updating shift. Please try again.');
      }
    });
  }

  goBack() {
    window.history.back();
  }
}
