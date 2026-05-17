import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Reservation, ReservationCreate, ReservationUpdate } from '../shared/models/reservation.model';

@Injectable({ providedIn: 'root' })
export class ReservationService {
  private readonly API = '/api/reservations';

  constructor(private http: HttpClient) {}

  getMy(status?: string): Observable<Reservation[]> {
    const params: any = {};
    if (status) params['status'] = status;
    return this.http.get<Reservation[]>(`${this.API}/my`, { params });
  }

  getByRestaurant(restaurantId: string, status?: string, dateFrom?: string, dateTo?: string): Observable<Reservation[]> {
    const params: any = {};
    if (status) params['status'] = status;
    if (dateFrom) params['date_from'] = dateFrom;
    if (dateTo) params['date_to'] = dateTo;
    return this.http.get<Reservation[]>(`${this.API}/restaurant/${restaurantId}`, { params });
  }

  getById(id: string): Observable<Reservation> {
    return this.http.get<Reservation>(`${this.API}/${id}`);
  }

  create(data: ReservationCreate): Observable<Reservation> {
    return this.http.post<Reservation>(this.API, data);
  }

  update(id: string, data: ReservationUpdate): Observable<Reservation> {
    return this.http.patch<Reservation>(`${this.API}/${id}`, data);
  }

  delete(id: string): Observable<void> {
    return this.http.delete<void>(`${this.API}/${id}`);
  }
}
