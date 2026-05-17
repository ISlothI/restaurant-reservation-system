import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ReservationSlot, SlotCreate, SlotUpdate } from '../shared/models/slot.model';

@Injectable({ providedIn: 'root' })
export class SlotService {
  private readonly API = '/api/restaurants';

  constructor(private http: HttpClient) {}

  getByRestaurant(restaurantId: string, status?: string): Observable<ReservationSlot[]> {
    const params: any = {};
    if (status) params['status'] = status;
    return this.http.get<ReservationSlot[]>(`${this.API}/${restaurantId}/slots`, { params });
  }

  getById(restaurantId: string, slotId: string): Observable<ReservationSlot> {
    return this.http.get<ReservationSlot>(`${this.API}/${restaurantId}/slots/${slotId}`);
  }

  create(restaurantId: string, data: SlotCreate): Observable<ReservationSlot> {
    return this.http.post<ReservationSlot>(`${this.API}/${restaurantId}/slots`, data);
  }

  update(restaurantId: string, slotId: string, data: SlotUpdate): Observable<ReservationSlot> {
    return this.http.put<ReservationSlot>(`${this.API}/${restaurantId}/slots/${slotId}`, data);
  }

  delete(restaurantId: string, slotId: string): Observable<void> {
    return this.http.delete<void>(`${this.API}/${restaurantId}/slots/${slotId}`);
  }
}
