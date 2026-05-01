import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-staff-list',
  template: `
    <div class="container">
      <div class="card">
        <div class="card-header" style="display: flex; justify-content: space-between; align-items: center;">
          <span>👥 Staff Management</span>
          <button class="btn btn-primary" (click)="showAddForm = !showAddForm">
            {{ showAddForm ? '✕ Cancel' : '+ Add Staff' }}
          </button>
        </div>

        <!-- Add/Edit Form -->
        <div *ngIf="showAddForm" class="card" style="background: #f8fafc;">
          <h3>{{ editingStaff ? 'Edit Staff' : 'Add New Staff' }}</h3>
          <form (ngSubmit)="saveStaff()">
            <div class="grid grid-2" style="margin-top: 1rem;">
              <div class="form-group">
                <label>Full Name</label>
                <input type="text" class="form-control" [(ngModel)]="formData.name" placeholder="John Doe" required>
              </div>
              <div class="form-group">
                <label>Email</label>
                <input type="email" class="form-control" [(ngModel)]="formData.email" placeholder="john@example.com">
              </div>
              <div class="form-group">
                <label>Role</label>
                <select class="form-control" [(ngModel)]="formData.role">
                  <option value="nurse">Nurse</option>
                  <option value="doctor">Doctor</option>
                  <option value="technician">Technician</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div class="form-group">
                <label>Phone</label>
                <input type="tel" class="form-control" [(ngModel)]="formData.phone" placeholder="+1234567890">
              </div>
            </div>
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem;">
              <button type="submit" class="btn btn-success">{{ editingStaff ? 'Update' : 'Add' }} Staff</button>
              <button type="button" class="btn btn-secondary" (click)="cancelForm()">Cancel</button>
            </div>
          </form>
        </div>

        <!-- Staff Table -->
        <div class="table-container" style="margin-top: 1.5rem;">
          <table>
            <thead>
              <tr>
                <th>Name</th>
                <th>Role</th>
                <th>Email</th>
                <th>Phone</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let staff of staffList">
                <td><strong>{{ staff.name }}</strong></td>
                <td><span class="badge" [ngClass]="'badge-' + staff.role">{{ staff.role }}</span></td>
                <td>{{ staff.email || '-' }}</td>
                <td>{{ staff.phone || '-' }}</td>
                <td>
                  <span class="badge" [ngClass]="staff.is_active ? 'badge-morning' : 'badge-off'">
                    {{ staff.is_active ? 'Active' : 'Inactive' }}
                  </span>
                </td>
                <td>
                  <button class="btn btn-primary" style="padding: 0.25rem 0.75rem; margin-right: 0.5rem;" (click)="editStaff(staff)">Edit</button>
                  <button class="btn btn-danger" style="padding: 0.25rem 0.75rem;" (click)="deleteStaff(staff.id)">Delete</button>
                </td>
              </tr>
              <tr *ngIf="staffList.length === 0">
                <td colspan="6" style="text-align: center; padding: 2rem; color: #64748b;">
                  No staff members found. Add one to get started!
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  `,
  imports: [CommonModule, FormsModule]
})
export class StaffListComponent implements OnInit {
  staffList: any[] = [];
  showAddForm = false;
  editingStaff: any = null;
  formData = {
    name: '',
    email: '',
    role: 'nurse',
    phone: ''
  };

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.loadStaff();
  }

  loadStaff() {
    this.http.get<any[]>('http://localhost:8000/api/v1/staff').subscribe({
      next: (data) => this.staffList = data,
      error: (err) => console.error('Error loading staff:', err)
    });
  }

  saveStaff() {
    if (this.editingStaff) {
      this.http.put(`http://localhost:8000/api/v1/staff/${this.editingStaff.id}`, this.formData).subscribe({
        next: () => {
          this.loadStaff();
          this.cancelForm();
        },
        error: (err) => console.error('Error updating staff:', err)
      });
    } else {
      this.http.post('http://localhost:8000/api/v1/staff', this.formData).subscribe({
        next: () => {
          this.loadStaff();
          this.cancelForm();
        },
        error: (err) => console.error('Error adding staff:', err)
      });
    }
  }

  editStaff(staff: any) {
    this.editingStaff = staff;
    this.formData = {
      name: staff.name,
      email: staff.email || '',
      role: staff.role,
      phone: staff.phone || ''
    };
    this.showAddForm = true;
  }

  deleteStaff(id: number) {
    if (confirm('Are you sure you want to delete this staff member?')) {
      this.http.delete(`http://localhost:8000/api/v1/staff/${id}`).subscribe({
        next: () => this.loadStaff(),
        error: (err) => console.error('Error deleting staff:', err)
      });
    }
  }

  cancelForm() {
    this.showAddForm = false;
    this.editingStaff = null;
    this.formData = { name: '', email: '', role: 'nurse', phone: '' };
  }
}
