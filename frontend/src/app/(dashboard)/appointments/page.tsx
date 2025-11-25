'use client';

import { Calendar } from "@/components/ui/calendar"
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useState } from "react";

export default function AppointmentsPage() {
  const [date, setDate] = useState<Date | undefined>(new Date())

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold tracking-tight">Appointments</h1>
      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Calendar</CardTitle>
          </CardHeader>
          <CardContent className="flex justify-center">
            <Calendar
              mode="single"
              selected={date}
              onSelect={setDate}
              className="rounded-md border"
            />
          </CardContent>
        </Card>
        <Card>
          <CardHeader>
            <CardTitle>Schedule for {date?.toDateString()}</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <p className="font-medium">09:00 AM</p>
                  <p className="text-sm text-muted-foreground">John Doe - General Checkup</p>
                </div>
                <div className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">Confirmed</div>
              </div>
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <p className="font-medium">10:30 AM</p>
                  <p className="text-sm text-muted-foreground">Jane Smith - Follow up</p>
                </div>
                <div className="bg-yellow-100 text-yellow-800 text-xs px-2 py-1 rounded">Pending</div>
              </div>
              <div className="flex items-center justify-between p-4 border rounded-lg">
                <div>
                  <p className="font-medium">02:00 PM</p>
                  <p className="text-sm text-muted-foreground">Mike Johnson - Consultation</p>
                </div>
                <div className="bg-green-100 text-green-800 text-xs px-2 py-1 rounded">Confirmed</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
