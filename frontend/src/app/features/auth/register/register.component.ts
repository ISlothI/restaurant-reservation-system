import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { AuthService } from '../../../core/auth.service';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterLink],
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  email = '';
  password = '';
  fullName = '';
  phone = '';
  role: 'guest' | 'admin' = 'guest';
  error = '';
  loading = false;

  constructor(private auth: AuthService, private router: Router) {}

  private formatRegisterError(detail: unknown): string {
    if (typeof detail === 'string') {
      return detail;
    }

    if (Array.isArray(detail)) {
      return detail
        .map((item) => this.formatValidationMessage(item))
        .join('; ');
    }

    return 'Regisztráció sikertelen';
  }

  private formatValidationMessage(item: unknown): string {
    if (!item || typeof item !== 'object') {
      return 'Érvénytelen adat';
    }

    const validationError = item as { loc?: unknown[]; msg?: string };
    const fieldName = Array.isArray(validationError.loc)
      ? validationError.loc[validationError.loc.length - 1]
      : undefined;
    const fieldLabel = this.getFieldLabel(
      typeof fieldName === 'string' ? fieldName : ''
    );

    if (fieldLabel && validationError.msg) {
      return `${fieldLabel}: ${validationError.msg}`;
    }

    return validationError.msg || 'Érvénytelen adat';
  }

  private getFieldLabel(fieldName: string): string {
    const labels: Record<string, string> = {
      email: 'E-mail',
      password: 'Jelszó',
      full_name: 'Teljes név',
      phone: 'Telefonszám',
      role: 'Szerepkör',
    };

    return labels[fieldName] || fieldName;
  }

  onSubmit(): void {
    this.loading = true;
    this.error = '';
    this.auth
      .register({
        email: this.email,
        password: this.password,
        full_name: this.fullName,
        phone: this.phone,
        role: this.role,
      })
      .subscribe({
        next: () => {
          this.loading = false;
          this.router.navigate(['/login']);
        },
        error: (err) => {
          this.loading = false;
          const detail = err.error?.detail;
          this.error = this.formatRegisterError(detail);
        },
      });
  }
}
