export interface ReservationSlot {
  id: string;
  restaurant_id: string;
  table_id: string;
  start_at: string;
  end_at: string;
  status: 'open' | 'closed';
}

export interface SlotCreate {
  table_id: string;
  start_at: string;
  end_at: string;
  status: 'open' | 'closed';
}

export interface SlotUpdate {
  table_id?: string;
  start_at?: string;
  end_at?: string;
  status?: 'open' | 'closed';
}
