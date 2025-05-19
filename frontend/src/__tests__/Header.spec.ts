// frontend/src/__tests__/Header.spec.ts
import { render, screen } from '@testing-library/svelte'
import { describe, it, expect } from 'vitest'
import Header from '../Header.svelte'

describe('Header.svelte', () => {
  it('renders logo and categories', () => {
    render(Header, {
      props: {
        categories: ['News', 'Sports'],
        activeCategory: 'News'
      }
    })

    expect(screen.getByTestId('logo')).toBeInTheDocument()
    expect(screen.getByText('News')).toBeInTheDocument()
    expect(screen.getByText('Sports')).toBeInTheDocument()
  })
})
