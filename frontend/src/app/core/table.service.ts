import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Table, TableCreate, TableUpdate } from '../shared/models/table.model';

@Injectable({ providedIn: 'root' })
export class TableService {
  private readonly API = '/api/restaurants';

  constructor(private http: HttpClient) {}

  getByRestaurant(restaurantId: string): Observable<Table[]> {
    return this.http.get<Table[]>(`${this.API}/${restaurantId}/tables`);
  }

  getById(restaurantId: string, tableId: string): Observable<Table> {
    return this.http.get<Table>(`${this.API}/${restaurantId}/tables/${tableId}`);
  }

  create(restaurantId: string, data: TableCreate): Observable<Table> {
    return this.http.post<Table>(`${this.API}/${restaurantId}/tables`, data);
  }

  update(restaurantId: string, tableId: string, data: TableUpdate): Observable<Table> {
    return this.http.put<Table>(`${this.API}/${restaurantId}/tables/${tableId}`, data);
  }

  delete(restaurantId: string, tableId: string): Observable<void> {
    return this.http.delete<void>(`${this.API}/${restaurantId}/tables/${tableId}`);
  }
}
