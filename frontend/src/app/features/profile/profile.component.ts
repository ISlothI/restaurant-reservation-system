import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../core/auth.service';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './profile.component.html',
})
export class ProfileComponent implements OnInit {
  form = { full_name: '', email: '', phone: '' };
  loading = false;
  error = '';
  success = '';

  constructor(public auth: AuthService) {}

  ngOnInit(): void {
    const u = this.auth.currentUser;
    if (u) {
      this.form = { full_name: u.full_name, email: u.email, phone: u.phone || '' };
    }
  }

  save(): void {
    this.loading = true;
    this.error = '';
    this.success = '';
    this.auth.updateProfile(this.form).subscribe({
      next: () => {
        this.loading = false;
        this.success = 'Profil sikeresen frissítve!';
      },
      error: (err) => {
        this.loading = false;
        const d = err.error?.detail;
        this.error = typeof d === 'string' ? d : 'Hiba a mentés során';
      },
    });
  }
}
