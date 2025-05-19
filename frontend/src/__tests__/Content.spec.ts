import { vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/svelte'
import Content from '../Content.svelte'
import * as api from '../lib/api'

// Fake articles payload
const fakeArticles = {
  response: {
    docs: [
      { _id: '1', headline: { main: 'T1' }, abstract: 'A1', multimedia: {}, word_count: 150 },
      { _id: '2', headline: { main: 'T2' }, abstract: 'A2', multimedia: {}, word_count: 300 },
    ]
  }
}

describe('Content.svelte', () => {
  beforeEach(() => {
    vi.spyOn(api, 'fetchArticles').mockResolvedValue(fakeArticles)
    vi.spyOn(api, 'fetchComments').mockResolvedValue([{ _id:'c1', content:'hi', removed:false }])
  })

  it('renders articles and read times', async () => {
    render(Content)
    // wait for fetchArticles to resolve
    await waitFor(() => expect(api.fetchArticles).toHaveBeenCalled())

    // Titles should appear
    expect(screen.getByText('T1')).toBeInTheDocument()
    expect(screen.getByText('T2')).toBeInTheDocument()

    // Read times: 1 MIN READ for first, 2 MIN READ for second
    expect(screen.getAllByText(/MIN READ/)[0]).toHaveTextContent('1 MIN READ')
    expect(screen.getAllByText(/MIN READ/)[1]).toHaveTextContent('2 MIN READ')
  })

  it('shows comment count and opens sidebar', async () => {
    render(Content)
    await waitFor(() => expect(api.fetchArticles).toHaveBeenCalled())

    const btns = screen.getAllByRole('button', { name: /comment/i })
    // Initially count is 1 (from our fakeComments)
    expect(btns[0].querySelector('.comment-count')!.textContent).toBe('1')

    // Clicking should call fetchComments again and display Comments component
    await fireEvent.click(btns[0])
    await waitFor(() => expect(api.fetchComments).toHaveBeenCalledWith('1'))
    expect(screen.getByText('hi')).toBeInTheDocument()
  })
})
