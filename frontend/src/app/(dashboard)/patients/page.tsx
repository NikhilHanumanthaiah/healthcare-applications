'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getPatients, createPatient, updatePatient, deletePatient } from '@/lib/api';
import { Patient, PatientCreate, PatientUpdate } from '@/types';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from '@/components/ui/dialog';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select"
import { Plus, Search, Pencil, Trash2, Eye } from 'lucide-react';
import { useState } from 'react';
import { toast } from 'sonner';

export default function PatientsPage() {
  const queryClient = useQueryClient();
  const [isOpen, setIsOpen] = useState(false);
  const [isEditMode, setIsEditMode] = useState(false);
  const [currentPatientId, setCurrentPatientId] = useState<string | null>(null);
  const [formData, setFormData] = useState<PatientCreate>({
    first_name: '',
    last_name: '',
    age: 0,
    gender: '',
    phone_number: '',
    email: '',
    address: '',
    date_of_birth: '',
    patient_type: 'ADULT',
    guardian_name: '',
    guardian_phone: '',
  });

  const { data: patients, isLoading, error } = useQuery({
    queryKey: ['patients'],
    queryFn: getPatients,
  });

  const createMutation = useMutation({
    mutationFn: createPatient,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] });
      setIsOpen(false);
      toast.success('Patient created successfully');
      resetForm();
    },
    onError: (err: any) => {
      toast.error('Failed to create patient: ' + (err.response?.data?.detail || err.message));
    },
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, data }: { id: string; data: PatientUpdate }) => updatePatient(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] });
      setIsOpen(false);
      toast.success('Patient updated successfully');
      resetForm();
    },
    onError: (err: any) => {
      toast.error('Failed to update patient: ' + (err.response?.data?.detail || err.message));
    },
  });

  const deleteMutation = useMutation({
    mutationFn: deletePatient,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['patients'] });
      toast.success('Patient deleted successfully');
    },
    onError: (err: any) => {
      toast.error('Failed to delete patient: ' + (err.response?.data?.detail || err.message));
    },
  });

  const resetForm = () => {
    setFormData({
      first_name: '',
      last_name: '',
      age: 0,
      gender: '',
      phone_number: '',
      email: '',
      address: '',
      date_of_birth: '',
      patient_type: 'ADULT',
      guardian_name: '',
      guardian_phone: '',
    });
    setIsEditMode(false);
    setCurrentPatientId(null);
  };

  const handleOpenChange = (open: boolean) => {
    setIsOpen(open);
    if (!open) {
      resetForm();
    }
  };

  const handleEdit = (patient: Patient) => {
    setFormData({
      first_name: patient.first_name,
      last_name: patient.last_name || '',
      age: patient.age,
      gender: patient.gender,
      phone_number: patient.phone_number || '',
      email: patient.email || '',
      address: patient.address || '',
      date_of_birth: patient.date_of_birth || '',
      patient_type: patient.patient_type,
      guardian_name: patient.guardian_name || '',
      guardian_phone: patient.guardian_phone || '',
    });
    setCurrentPatientId(patient.patient_id);
    setIsEditMode(true);
    setIsOpen(true);
  };

  const handleDelete = (id: string) => {
    if (confirm('Are you sure you want to delete this patient?')) {
      deleteMutation.mutate(id);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Sanitize form data: convert empty strings to null/undefined for optional fields
    const cleanedData = Object.fromEntries(
      Object.entries(formData).map(([key, value]) => {
        if (value === '') {
          return [key, null];
        }
        return [key, value];
      })
    ) as PatientCreate; // Cast back to PatientCreate/Update

    if (isEditMode && currentPatientId) {
      // For update, we might want to remove keys that are null if the backend ignores them,
      // but sending null usually means "unset" or "clear". 
      // However, the user said "if nothing is filled then it shouldnot send anything".
      // So we should probably filter out empty strings entirely or send null.
      // The backend Pydantic model has Optional fields defaulting to None.
      // If we send null, Pydantic accepts it.
      // If we send "", Pydantic might error or treat it as empty string.
      // Let's try sending null for now as per standard JSON API practices, 
      // OR better yet, remove the keys that are empty strings if we want "partial update" behavior 
      // where missing keys are ignored.
      // But wait, if I want to CLEAR a field (e.g. remove email), I MUST send null.
      // If I just want to leave it alone, I shouldn't include it?
      // The current logic loads ALL data into the form. So if I leave it as is, it sends the original value.
      // If I clear it, it becomes "".
      // So "" means "user cleared this field". So I should send null.
      
      updateMutation.mutate({ id: currentPatientId, data: cleanedData });
    } else {
      createMutation.mutate(cleanedData);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Patients</h1>
          <p className="text-muted-foreground">Manage patient records and history.</p>
        </div>
        <Dialog open={isOpen} onOpenChange={handleOpenChange}>
          <DialogTrigger asChild>
            <Button onClick={() => { setIsEditMode(false); resetForm(); }}>
              <Plus className="mr-2 h-4 w-4" /> Add Patient
            </Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[600px] max-h-[90vh] overflow-y-auto">
            <DialogHeader>
              <DialogTitle>{isEditMode ? 'Edit Patient' : 'Add New Patient'}</DialogTitle>
              <DialogDescription>
                {isEditMode ? 'Update the patient details below.' : 'Enter the patient\'s details here. Click save when you\'re done.'}
              </DialogDescription>
            </DialogHeader>
            <form onSubmit={handleSubmit}>
              <div className="grid gap-4 py-4">
                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="first_name">First Name *</Label>
                    <Input
                      id="first_name"
                      value={formData.first_name}
                      onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="last_name">Last Name</Label>
                    <Input
                      id="last_name"
                      value={formData.last_name || ''}
                      onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="age">Age *</Label>
                    <Input
                      id="age"
                      type="number"
                      value={formData.age || ''}
                      onChange={(e) => setFormData({ ...formData, age: parseInt(e.target.value) || 0 })}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="gender">Gender *</Label>
                    <Select 
                      value={formData.gender} 
                      onValueChange={(value) => setFormData({ ...formData, gender: value })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select gender" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="male">Male</SelectItem>
                        <SelectItem value="female">Female</SelectItem>
                        <SelectItem value="other">Other</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="phone">Phone *</Label>
                    <Input
                      id="phone"
                      value={formData.phone_number}
                      onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                      required
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="email">Email</Label>
                    <Input
                      id="email"
                      type="email"
                      value={formData.email || ''}
                      onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    />
                  </div>
                </div>

                <div className="grid gap-2">
                  <Label htmlFor="address">Address</Label>
                  <Input
                    id="address"
                    value={formData.address || ''}
                    onChange={(e) => setFormData({ ...formData, address: e.target.value })}
                  />
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="dob">Date of Birth</Label>
                    <Input
                      id="dob"
                      type="date"
                      value={formData.date_of_birth || ''}
                      onChange={(e) => setFormData({ ...formData, date_of_birth: e.target.value })}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="type">Patient Type</Label>
                     <Select 
                      value={formData.patient_type} 
                      onValueChange={(value) => setFormData({ ...formData, patient_type: value })}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select type" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="ADULT">Adult</SelectItem>
                        <SelectItem value="CHILD">Child</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-4">
                  <div className="grid gap-2">
                    <Label htmlFor="guardian_name">Guardian Name</Label>
                    <Input
                      id="guardian_name"
                      value={formData.guardian_name || ''}
                      onChange={(e) => setFormData({ ...formData, guardian_name: e.target.value })}
                    />
                  </div>
                  <div className="grid gap-2">
                    <Label htmlFor="guardian_phone">Guardian Phone</Label>
                    <Input
                      id="guardian_phone"
                      value={formData.guardian_phone || ''}
                      onChange={(e) => setFormData({ ...formData, guardian_phone: e.target.value })}
                    />
                  </div>
                </div>

              </div>
              <DialogFooter>
                <Button type="submit" disabled={createMutation.isPending || updateMutation.isPending}>
                  {createMutation.isPending || updateMutation.isPending ? 'Saving...' : 'Save changes'}
                </Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>

      <div className="rounded-md border bg-card">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Age</TableHead>
              <TableHead>Gender</TableHead>
              <TableHead>Phone</TableHead>
              <TableHead>Type</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {isLoading ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10">
                  Loading patients...
                </TableCell>
              </TableRow>
            ) : error ? (
               <TableRow>
                <TableCell colSpan={6} className="text-center py-10 text-red-500">
                  Error loading patients. Is the backend running?
                </TableCell>
              </TableRow>
            ) : patients?.length === 0 ? (
              <TableRow>
                <TableCell colSpan={6} className="text-center py-10">
                  No patients found.
                </TableCell>
              </TableRow>
            ) : (
              patients?.map((patient) => (
                <TableRow key={patient.patient_id}>
                  <TableCell className="font-medium">
                    {patient.first_name} {patient.last_name}
                  </TableCell>
                  <TableCell>{patient.age}</TableCell>
                  <TableCell className="capitalize">{patient.gender}</TableCell>
                  <TableCell>{patient.phone_number}</TableCell>
                  <TableCell>{patient.patient_type}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                        <Button variant="ghost" size="icon" onClick={() => handleEdit(patient)}>
                            <Pencil className="h-4 w-4" />
                        </Button>
                        <Button variant="ghost" size="icon" className="text-red-500 hover:text-red-600" onClick={() => handleDelete(patient.patient_id)}>
                            <Trash2 className="h-4 w-4" />
                        </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </div>
    </div>
  );
}
