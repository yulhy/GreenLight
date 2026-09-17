export interface CatalogItem {
  item_id: string;
  category: string;
  item_name: string;

  unit: string;
  unit_price_krw: number;

  currency?: string | null;
  price_type?: string | null;
  pricing_method?: string | null;

  fuel_type?: string | null;

  fuel_price_per_liter?:
    number | null;

  fuel_efficiency_km_per_liter?:
    number | null;

  distance_km?: number | null;

  cost_source?: string | null;
  source_url?: string | null;
  source_date?: string | null;
  cost_notes?: string | null;

  original_unit?: string | null;

  original_unit_price_krw?:
    number | null;

  standardization_note?:
    string | null;
}


export interface CatalogCategoriesResponse {
  categories: string[];
}


export interface CatalogItemsResponse {
  items: CatalogItem[];
}