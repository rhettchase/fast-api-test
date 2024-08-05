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
  async ({ question_id, response }) => {
    const res = await fetch(`http://localhost:8000/api/v1/answers/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question_id, response }),
    });
    if (!res.ok) {
      throw new Error('Failed to submit response');
    }
    return res.json();
  }
);

// Fetch next question based on the response
export const fetchNextQuestion = createAsyncThunk(
  'form/fetchNextQuestion',
  async ({ question_id, response }) => {
    const res = await fetch(`http://localhost:8000/api/v1/next-question/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ question_id, response }),
    });
    if (!res.ok) {
      throw new Error('Failed to fetch next question');
    }
    return res.json();
  }
);

// Redux slice
const formSlice = createSlice({
  name: 'form',
  initialState: {
    currentFormId: 1,
    formConfig: null, // Initially null
    message: '',
    userResponse: null, // Track the current user response
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
        state.message =
          action.payload.message || 'Response submitted successfully';
      })
      .addCase(submitUserResponse.rejected, (state) => {
        state.message = 'Failed to submit response';
      })
      .addCase(fetchNextQuestion.fulfilled, (state, action) => {
        // Assume action.payload contains the new question structure
        if (typeof action.payload === 'object' && action.payload.options) {
          state.formConfig = {
            title: 'Dynamic Questionnaire', // or any other title logic
            fields: [
              {
                name: `question${action.payload.id}`,
                type: 'string',
                label: action.payload.text,
                options: action.payload.options,
              },
            ],
          };
          state.message = '';
        } else if (typeof action.payload === 'string') {
          state.message = action.payload; // Set message when it's a string
        }
      })
      .addCase(fetchNextQuestion.rejected, (state) => {
        state.message = 'Failed to fetch next question';
      });
  },
});

export const { setUserResponse } = formSlice.actions;
export default formSlice.reducer;
