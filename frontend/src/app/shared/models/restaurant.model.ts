export interface Restaurant {
  id: string;
  manager_id: string;
  name: string;
  description: string;
  address: string;
  contact: string;
  opening_hours: string;
  services: string[];
  is_active: boolean;
}

export interface RestaurantCreate {
  name: string;
  description: string;
  address: string;
  contact: string;
  opening_hours: string;
  services: string[];
  is_active: boolean;
}

export interface RestaurantUpdate {
  name?: string;
  description?: string;
  address?: string;
  contact?: string;
  opening_hours?: string;
  services?: string[];
  is_active?: boolean;
}
