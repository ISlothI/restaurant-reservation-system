export interface Reservation {
  id: string;
  restaurant_id: string;
  user_id: string;
  slot_id: string;
  party_size: number;
  status: 'pending' | 'confirmed' | 'cancelled';
  special_occasion: string | null;
  guest_note: string;
  created_at: string;
  updated_at: string;
  restaurant_name?: string;
  table_name?: string;
  table_type?: string;
  slot_start?: string;
  slot_end?: string;
  user_name?: string;
}

export interface ReservationCreate {
  restaurant_id: string;
  slot_id: string;
  party_size: number;
  special_occasion: string | null;
  guest_note: string;
}

export interface ReservationUpdate {
  status?: 'pending' | 'confirmed' | 'cancelled';
  slot_id?: string;
  party_size?: number;
  special_occasion?: string | null;
  guest_note?: string;
}
