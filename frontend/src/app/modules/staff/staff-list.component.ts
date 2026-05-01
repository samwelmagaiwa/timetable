import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-staff-list',
  template: `
    <h2>Staff List</h2>
    <button (click)="addStaff()">Add Staff</button>
    <ul>
      <li *ngFor="let staff of staffList">
        {{ staff.name }} ({{ staff.role }})
        <button (click)="editStaff(staff.id)">Edit</button>
        <button (click)="deleteStaff(staff.id)">Delete</button>
      </li>
    </ul>
  `
})
export class StaffListComponent implements OnInit {
  staffList: any[] = [];
  
  constructor(private http: HttpClient) {}
  
  ngOnInit() {
    this.loadStaff();
  }
  
  loadStaff() {
    this.http.get<any[]>('http://localhost:8000/api/v1/staff').subscribe(data => {
      this.staffList = data;
    });
  }
  
  addStaff() { /* TODO */ }
  editStaff(id: number) { /* TODO */ }
  deleteStaff(id: number) { /* TODO */ }
}
