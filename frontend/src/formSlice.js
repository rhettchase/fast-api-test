// formSlice.js
import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Fetch form configuration
export const fetchFormConfig = createAsyncThunk(
  'form/fetchConfig',
  async (formId) => {
    const response = await fetch(
      `http://localhost:8000/api/v1/form-config/${formId}`
    );
    if (!response.ok) {
      throw new Error('Failed to fetch form config');
    }
    return response.json();
  }
);

// Submit user response
export const submitUserResponse = createAsyncThunk(
  'form/submitResponse',
  async ({ questionId, response }) => {
    const res = await fetch(`http://localhost:8000/api/v1/answers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question_id: questionId, response }),
    });
    if (!res.ok) {
      throw new Error('Failed to submit response');
    }
    return res.json();
  }
);

// Redux slice
const formSlice = createSlice({
  name: 'form',
  initialState: {
    currentFormId: 1, // Or whatever logic you use to set this
    formConfig: null,
    message: '',
    userResponse: null,
  },
  reducers: {
    setUserResponse(state, action) {
      state.userResponse = action.payload;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFormConfig.fulfilled, (state, action) => {
        state.formConfig = action.payload;
        state.message = '';
      })
      .addCase(fetchFormConfig.rejected, (state) => {
        state.message = 'Failed to load form configuration';
      })
      .addCase(submitUserResponse.fulfilled, (state, action) => {
        state.message = action.payload.message || '';
      })
      .addCase(submitUserResponse.rejected, (state) => {
        state.message = 'Failed to submit response';
      });
  },
});

export const { setUserResponse } = formSlice.actions;
export default formSlice.reducer;
