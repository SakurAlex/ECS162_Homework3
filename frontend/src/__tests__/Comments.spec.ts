// frontend/src/__tests__/Content.spec.ts
import { render, fireEvent, screen } from '@testing-library/svelte'
import { describe, it, expect, vi } from 'vitest'
import Content from '../Content.svelte'

describe('Content.svelte', () => {
  const articles = [
    { id: 1, title: 'Hello World', readTime: '3 min', commentsCount: 5 }
  ]

  it('renders title and read time', () => {
    render(Content, { props: { articles } })
    expect(screen.getByText('Hello World')).toBeInTheDocument()
    expect(screen.getByText('3 min')).toBeInTheDocument()
  })

  it('shows comments count and fires openSidebar event', async () => {
    const { component } = render(Content, { props: { articles } })
    const opener = vi.fn()
    component.$on('openSidebar', opener)

    const countEl = screen.getByText('5 comments')
    await fireEvent.click(countEl)

    expect(opener).toHaveBeenCalledOnce()
    expect(opener.mock.calls[0][0].detail).toBe(1)
  })
})
