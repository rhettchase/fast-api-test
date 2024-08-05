import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

// Fetch form configuration
export const fetchFormConfig = createAsyncThunk(
  'form/fetchConfig',
  async (formId) => {
    if (formId === null) return null; // Skip fetching if formId is null
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
    setMessage(state, action) {
      state.message = action.payload;
    },
    clearFormConfig(state) {
      state.formConfig = null;
      state.currentFormId = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchFormConfig.fulfilled, (state, action) => {
        if (action.payload === null) {
          state.formConfig = null;
          return;
        }
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
        const payload = action.payload;

        if (typeof payload === 'object') {
          if (payload.options) {
            // If payload contains options, it's a new question
            state.formConfig = {
              title: 'Dynamic Questionnaire',
              fields: [
                {
                  name: `question${payload.id}`,
                  type: 'string',
                  label: payload.text,
                  options: payload.options,
                },
              ],
            };
            state.currentFormId = payload.id || state.currentFormId; // Update current form ID if valid
            state.message = '';
          } else if (payload.message) {
            // If payload has a message, display it
            state.message = payload.message;
            state.formConfig = null; // Clear formConfig if no more questions
            state.currentFormId = null; // Set currentFormId to null as there are no more questions
          }
        }
      })
      .addCase(fetchNextQuestion.rejected, (state) => {
        state.message = 'Failed to fetch next question';
      });
  },
});

export const { setUserResponse, setMessage, clearFormConfig } = formSlice.actions;
export default formSlice.reducer;
