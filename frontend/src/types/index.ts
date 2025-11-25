export interface Patient {
    patient_id: string;
    first_name: string;
    last_name?: string | null;
    date_of_birth?: string | null;
    age: number;
    gender: string;
    phone_number?: string | null;
    email?: string | null;
    address?: string | null;
    create_at: string;
    updated_at: string;
    is_active: boolean;
    patient_type: string;
    guardian_name?: string | null;
    guardian_phone?: string | null;
}

export interface PatientCreate {
    first_name: string;
    last_name?: string | null;
    age: number;
    gender: string;
    phone_number: string;
    email?: string | null;
    address?: string | null;
    date_of_birth?: string | null;
    patient_type?: string;
    guardian_name?: string | null;
    guardian_phone?: string | null;
}

export interface PatientUpdate {
    first_name?: string | null;
    last_name?: string | null;
    age?: number | null;
    gender?: string | null;
    phone_number?: string | null;
    email?: string | null;
    address?: string | null;
    date_of_birth?: string | null;
    patient_type?: string | null;
    guardian_name?: string | null;
    guardian_phone?: string | null;
}

export interface Medicine {
    id?: number;
    name: string;
    price_per_unit: number;
    stock: number;
}

export interface BillItem {
    medicine_id: number;
    quantity: number;
    price_per_unit?: number;
}

export interface Bill {
    id?: number;
    patient_name: string;
    patient_age: number;
    items: BillItem[];
    total_amount?: number;
}

export interface User {
    id: string;
    name: string;
    email: string;
    role: 'admin' | 'doctor' | 'patient';
}
