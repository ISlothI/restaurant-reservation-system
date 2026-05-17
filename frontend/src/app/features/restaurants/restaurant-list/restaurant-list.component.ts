import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterLink } from '@angular/router';
import { RestaurantService } from '../../../core/restaurant.service';
import { Restaurant } from '../../../shared/models/restaurant.model';
import { AuthService } from '../../../core/auth.service';

@Component({
  selector: 'app-restaurant-list',
  standalone: true,
  imports: [CommonModule, RouterLink],
  templateUrl: './restaurant-list.component.html',
})
export class RestaurantListComponent implements OnInit {
  restaurants: Restaurant[] = [];
  loading = true;

  constructor(
    private restaurantService: RestaurantService,
    public auth: AuthService
  ) {}

  ngOnInit(): void {
    this.restaurantService.getAll().subscribe({
      next: (data) => {
        this.restaurants = data;
        this.loading = false;
      },
      error: () => {
        this.loading = false;
      },
    });
  }

  serviceLabel(service: string): string {
    const map: Record<string, string> = {
      outdoor_seating: 'Terasz',
      vegan_options: 'Vegán ételek',
      gluten_free_options: 'Gluténmentes',
      wheelchair_accessible: 'Akadálymentes',
      pet_friendly: 'Kisállatbarát',
    };
    return map[service] || service;
  }
}
