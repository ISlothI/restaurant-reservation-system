export interface Table {
  id: string;
  restaurant_id: string;
  name: string;
  capacity: number;
  table_type: 'indoor' | 'outdoor' | 'window';
  is_active: boolean;
}

export interface TableCreate {
  name: string;
  capacity: number;
  table_type: 'indoor' | 'outdoor' | 'window';
  is_active: boolean;
}

export interface TableUpdate {
  name?: string;
  capacity?: number;
  table_type?: 'indoor' | 'outdoor' | 'window';
  is_active?: boolean;
}
