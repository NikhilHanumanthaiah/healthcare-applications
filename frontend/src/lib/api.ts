import api from './axios';
import { Patient, PatientCreate, PatientUpdate, Medicine, Bill } from '@/types';

export const getPatients = async (): Promise<Patient[]> => {
    const response = await api.get('/patients');
    return response.data;
};

export const getPatient = async (id: string): Promise<Patient> => {
    const response = await api.get(`/patient/${id}`);
    return response.data;
};

export const createPatient = async (data: PatientCreate): Promise<Patient> => {
    const response = await api.post('/patient', data);
    return response.data;
};

export const updatePatient = async (id: string, data: PatientUpdate): Promise<Patient> => {
    const response = await api.put(`/patient/${id}`, data);
    return response.data;
};

export const deletePatient = async (id: string): Promise<void> => {
    await api.delete(`/patient/${id}`);
};

export const getMedicines = async (): Promise<Medicine[]> => {
    const response = await api.get('/medicines');
    return response.data;
};

export const createMedicine = async (data: Medicine): Promise<Medicine> => {
    const response = await api.post('/medicines', data);
    return response.data;
};

export const updateMedicine = async (id: number, data: Partial<Medicine>): Promise<Medicine> => {
    const response = await api.patch(`/medicines/${id}`, data);
    return response.data;
};

export const deleteMedicine = async (id: number): Promise<void> => {
    await api.delete(`/medicines/${id}`);
};

export const getBills = async (): Promise<Bill[]> => {
    const response = await api.get('/bills');
    return response.data;
};

export const createBill = async (data: Bill): Promise<Bill> => {
    const response = await api.post('/bills', data);
    return response.data;
};
