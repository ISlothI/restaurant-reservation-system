import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Restaurant, RestaurantCreate, RestaurantUpdate } from '../shared/models/restaurant.model';

@Injectable({ providedIn: 'root' })
export class RestaurantService {
  private readonly API = '/api/restaurants';

  constructor(private http: HttpClient) {}

  getAll(): Observable<Restaurant[]> {
    return this.http.get<Restaurant[]>(this.API);
  }

  getById(id: string): Observable<Restaurant> {
    return this.http.get<Restaurant>(`${this.API}/${id}`);
  }

  getMyRestaurant(): Observable<Restaurant | null> {
    return this.http.get<Restaurant | null>(`${this.API}/my/restaurant`);
  }

  create(data: RestaurantCreate): Observable<Restaurant> {
    return this.http.post<Restaurant>(this.API, data);
  }

  update(id: string, data: RestaurantUpdate): Observable<Restaurant> {
    return this.http.put<Restaurant>(`${this.API}/${id}`, data);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}`);
  }
}
