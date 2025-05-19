// frontend/src/__tests__/api.spec.ts
import { describe, it, expect, vi } from 'vitest'
import * as api from '../lib/api'

global.fetch = vi.fn()

describe('api.ts', () => {
  afterEach(() => {
    vi.resetAllMocks()
  })

  it('fetches articles from /api/ucdavis-news', async () => {
    const mockData = { data: [{ id: 1, title: 'Test Article' }] }
    // @ts-ignore
    fetch.mockResolvedValueOnce({ json: () => Promise.resolve(mockData) })

    const result = await api.fetchArticles()
    expect(fetch).toHaveBeenCalledWith('/api/ucdavis-news', { credentials: 'include' })
    expect(result).toEqual(mockData)     // ← expect the full object
  })

  it('fetches comments for a given article', async () => {
    const mockComments = { data: [{ id: 2, text: 'Hi' }] }
    // @ts-ignore
    fetch.mockResolvedValueOnce({ json: () => Promise.resolve(mockComments) })

    const result = await api.fetchComments('123')
    expect(fetch).toHaveBeenCalledWith('/api/comments?article_id=123', { credentials: 'include' })
    expect(result).toEqual(mockComments)  // ← and here, too
  })

  it('posts a comment', async () => {
    const mockResp = { success: true }
    // @ts-ignore
    fetch.mockResolvedValueOnce({ json: () => Promise.resolve(mockResp) })

    const result = await api.postComment('123', 'Hello!')
    expect(fetch).toHaveBeenCalledWith(
      '/api/comments',
      expect.objectContaining({
        method: 'POST',
        credentials: 'include',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ article_id: '123', content: 'Hello!' })
      })
    )
    expect(result).toEqual(mockResp)
  })

  it('deletes a comment', async () => {
    // @ts-ignore
    fetch.mockResolvedValueOnce({})
    await api.deleteComment('987')
    expect(fetch).toHaveBeenCalledWith(
      '/api/comments/987',
      { method: 'DELETE', credentials: 'include' }
    )
  })
})
